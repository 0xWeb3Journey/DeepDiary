# face_operation.py
# force on dealing with Face model
import logging

from django.db import transaction

from library.models import Face, Kps, FaceLandmarks3D, FaceLandmarks2D
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function, highlight_color, end_color

logger = logging.getLogger(__name__)


class FaceOperation(BaseOperation):

    def __init__(self, img_instance=None):
        super().__init__(Face, img_instance)
        self.profile = None

    @trace_function
    def save(self, data, *args, **kwargs) -> None:
        """
        将人脸检测数据保存到数据库。
        """
        # 保存逻辑...
        if not self.check_data_validity(data):
            print(f"No face data to process for img {self.img_instance.id}.")
            return

        # 从**kwargs获取profile
        faces = data.get('face', None)
        profiles = data.get('profiles', None)

        kps_to_create = []
        landmarks3d_to_create = []
        landmarks2d_to_create = []

        for idx, fc_data in enumerate(faces):  # data 是个人脸列表
            face_instance = self.create_face_instance(fc_data['fc'], profile=profiles[idx] if profiles else None)

            # 创建Kps、FaceLandmarks3D、FaceLandmarks2D相关对象列表
            kps_to_create.extend(self.create_kps_list(face_instance, fc_data['kps']))
            landmarks3d_to_create.extend(self.create_landmarks3d_list(face_instance, fc_data['landmarks3d']))
            landmarks2d_to_create.extend(self.create_landmarks2d_list(face_instance, fc_data['landmarks2d']))

        # 批量创建其他相关对象
        Kps.objects.bulk_create(kps_to_create)
        FaceLandmarks3D.objects.bulk_create(landmarks3d_to_create)
        FaceLandmarks2D.objects.bulk_create(landmarks2d_to_create)

        print(f"Face data saved for img {self.img_instance.id}.")

    def clear(self):
        """
        清除已存在的人脸数据。
        """
        Face.objects.filter(img=self.img_instance).delete()

    def create_kps_list(self, face, kps_data_list):
        kps_to_create = []
        for kps_data in kps_data_list:
            kps_to_create.append(Kps(face=face, x=kps_data[0], y=kps_data[1]))
        return kps_to_create

    def create_landmarks3d_list(self, face, landmarks3d_data_list):
        landmarks3d_to_create = []
        for landmark_data in landmarks3d_data_list:
            landmarks3d_to_create.append(FaceLandmarks3D(
                face=face, x=landmark_data[0], y=landmark_data[1], z=landmark_data[2]))
        return landmarks3d_to_create

    def create_landmarks2d_list(self, face, landmarks2d_data_list):
        landmarks2d_to_create = []
        for landmark_data in landmarks2d_data_list:
            landmarks2d_to_create.append(FaceLandmarks2D(
                face=face, x=landmark_data[0], y=landmark_data[1]))
        return landmarks2d_to_create

    @trace_function
    def create_face_instance(self, fc, profile=None):
        src = fc.pop('src', None)  # 移除并保存src字段
        fc['img'] = self.img_instance
        fc['profile'] = profile
        try:
            # 先保存不包含src的其他字段
            face_instance = Face.objects.create(**fc)
            print(f"Face instance without src created: {face_instance.id}.")

            # 更新src字段
            if src:
                face_instance.src = src
                face_instance.save(update_fields=['src'])
                print(f"{highlight_color}Face instance with src created: {face_instance.profile.name}.{end_color}")
                src.close()

        except Exception as e:
            # 记录错误和异常处理
            logger.error(f'Error creating Face instance: {e}')
            return None

        return face_instance

    def get_category_data(self):
        """
        获取分类数据。
        """
        names = self.img_instance.profiles.order_by('name').values_list('name', flat=True)
        name_cnt = len(names)  # 使用 len() 获取数量，更直观且避免额外的数据库查询

        # 根据不同的名字数量，生成不同的分类描述
        if name_cnt == 0:
            name_str = 'no face'
        elif name_cnt <= 5:
            name_str = ' '.join(names)
        else:
            name_str = 'group face'

        # 构建并返回分类数据
        return {
            'group': ['group', name_str]
        }
