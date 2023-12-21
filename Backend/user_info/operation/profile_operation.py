# profile_operation.py
# force on dealing with Profile model
import numpy as np
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from sklearn.metrics.pairwise import cosine_similarity

from deep_diary.settings import calib
from user_info.models import Profile
from user_info.operation.base_operation import BaseOperation
from utilities.common import get_pinyin
import logging

logger = logging.getLogger(__name__)


class ProfileOperation(BaseOperation):
    def __init__(self, profile_instance=None):
        super().__init__(Profile, profile_instance)

    def get_or_create_profile(self, data, name=None):  # data是face数据， 字典类型
        # 如果没有提供名字，就使用face中的name
        name = data.get('profile', None) if name is None else None

        # 如果没有得到正确的名字，只有'Unknown', 'Unknown'，则返回None
        if not name:
            return None

        full_pinyin, lazy_pinyin = get_pinyin(name)
        creation_params = {
            'username': self.generate_unique_username(name),
            'password': make_password('deep-diary666'),
            'name': name,
            'full_pinyin': full_pinyin,
            'lazy_pinyin': lazy_pinyin,
            'avatar': data['src'],
            'embedding': data['embedding'],
        }

        try:
            profile, created = Profile.objects.get_or_create(
                name=name,
                defaults=creation_params
            )
            if created:
                print(f'INFO: Created a new profile: {profile.name}')
            else:
                print(f'INFO: The profile already existed: {profile.name}')
            return profile
        except Profile.MultipleObjectsReturned:
            print('WARNING: Multiple profiles found with the name:', name)
            return Profile.objects.filter(name=name).first()
        except IntegrityError:
            print('ERROR: Failed to create a new profile due to an IntegrityError.')
            return None

    def get_profiles(self, face_datas):
        """
        获取人脸数据对应的profile列表。
        """
        profiles = []
        for face_data in face_datas:
            profile = self.get_or_create_profile(face_data)
            profile = profile if isinstance(profile, Profile) else None
            if profile:
                profiles.append(profile)
        return profiles

    @staticmethod
    def generate_unique_username(name):
        base_username = name
        username = base_username
        counter = 0
        while Profile.objects.filter(username=username).exists():
            counter += 1
            username = f'{base_username}_{counter}'
        return username

    def face_rename(self, face_instance, new_name=None):
        if new_name is None:
            print(f'INFO: No new name provided for face renaming')
            return None, face_instance

        data = {
            'profile': new_name,
            'src': face_instance.src,
            'embedding': face_instance.embedding,
        }

        profile, created = self.get_or_create_profile(data, name=new_name)
        old_name = face_instance.profile.name if face_instance.profile else 'Unknown'
        print(f'INFO: Renaming face from {old_name} to {new_name}')
        face_instance.profile = profile
        face_instance.save()

        return profile, face_instance

    @staticmethod
    def face_recognition(embedding):  # 'instance', serializers
        profile = None
        face_score = 0
        # 1. 提取出Profile模型中所有embedding，记作embeddings，并进行转换
        profiles = Profile.objects.exclude(name__startswith='unknown')
        print(f'INFO: the named profiles count is {profiles.count()}')
        embeddings = profiles.values_list('embedding', flat=True)
        embeddings = [np.frombuffer(embedding, dtype=np.float16) for embedding in embeddings if embedding]

        # 判断embedding是否为空
        if len(embeddings) == 0:
            print('embeddings is empty')
            return None, 0

        # 转换为矩阵形式进行相似度计算
        embeddings_matrix = np.stack(embeddings)
        # print(embeddings_matrix.shape)
        # print(embedding.reshape(1, -1).shape)
        similarity_scores = cosine_similarity(embedding.reshape(1, -1), embeddings_matrix)

        # 找到最大相似度对应的索引
        max_similarity_index = np.argmax(similarity_scores)
        max_similarity_score = similarity_scores[0, max_similarity_index]

        # print(similarity_scores, max_similarity_index, max_similarity_score)

        # 如果top1相似度>0.4，则更新profile和face_score
        if max_similarity_score > calib['face']['reco_threshold']:
            profile = profiles[int(max_similarity_index)]
            face_score = max_similarity_score
            print(f'INFO: recognition result: {profile}--', face_score)
        else:
            # 新创建一个profile
            print(f'INFO: recognition result: unknown--', face_score)

        return profile, face_score

    def get_pinyin(self):
        try:
            self.profile_instance.full_pinyin, self.profile_instance.lazy_pinyin = get_pinyin(
                self.profile_instance.name)
            self.profile_instance.save()
        except Exception as e:
            # 处理异常（例如：日志记录）
            logger.error(f"Error while getting pinyin: {e}")
        return self.profile_instance

    def get_pinyin(self):
        try:
            self.profile_instance.full_pinyin, self.profile_instance.lazy_pinyin = get_pinyin(
                self.profile_instance.name)
            self.profile_instance.save()
        except Exception as e:
            # 处理异常（例如：日志记录）
            logger.error(f"Error while getting pinyin: {e}")
        return self.profile_instance

