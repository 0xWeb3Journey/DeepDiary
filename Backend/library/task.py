import bisect
import random
import string
from datetime import datetime
from io import BytesIO

import clip
import cv2
import numpy as np
import pyexiv2
import torch
from PIL import Image
from celery import shared_task
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction, IntegrityError
from django.db.models import F
from insightface.app import FaceAnalysis
from lavis.models import load_model_and_preprocess
from sklearn.metrics.pairwise import cosine_similarity

from deep_diary.settings import cfg, calib
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.imagga import imagga_get
from library.models import Img, Category, Face, \
    FaceLandmarks3D, FaceLandmarks2D, Kps, Stat, Address, Evaluate, Date
from library.serializers import McsDetailSerializer, ColorSerializer, ColorBackgroundSerializer, \
    ColorForegroundSerializer, ColorImgSerializer, FaceSerializer
from user_info.models import Profile, Assert
from user_info.task import ProfileProcess
from utils.mcs_storage import upload_file_pay
from utils.utils import get_pinyin

color_palette = {
    "beige": '#e0c4b2',
    "hot pink": '#c73d77',
    "magenta": '#a7346e',
    "red": '#ae2935',
    "black": '#39373b',
    "teal": '#426972',
    "lavender": '#6a6378',
    "maroon": '#6c2135',
    "blue": '#2f5e97',
    "light blue": '#99b1cb',
    "mauve": '#ac6075',
    "turquoise": '#38afcd',
    "brown": '#574039',
    "navy blue": '#2b2e43',
    "violet": '#473854',
    "dark green": '#176352',
    "light brown": '#ac8a64',
    "orange": '#e2855e',
    "white": '#f4f5f0',
    "gold": '#dcba60',
    "light green": '#aec98e',
    "pink": '#e3768c',
    "yellow": '#ebd07f',
    "green": '#359369',
    "olive green": '#7f8765',
    "plum": '#58304e',
    "skin": '#bd9769',
    "greige": '#a4b39f',
    "light grey": '#bcb8b8',
    "purple": '#875287',
    "grey": '#8c8c8c',
    "light pink": '#e6c1be',
}


# IMG_FUC_LIST = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories', 'get_faces', 'get_caption',
#                 'get_feature']
#
# IMG_ADD_LIST = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
#                 'add_colors_to_category', 'add_layout_to_category', 'add_size_to_category']


class ImgProces:
    def __init__(self, path=None, instance=None, procedure=None):
        """
        path: 图片路径， 可以是本地的，也可以是云存储的, 相对于 media 文件夹的路径
        instance: 图片实体
        procedure: 处理流程，为列表格式['face', 'object', 'caption', 'key point', 'extraction', 'auto tag', 'color', 'classification']
        """
        self.app = None
        if procedure is None:
            procedure = ['face', 'object', 'caption', 'key point', 'extraction', 'auto tag', 'color', 'classification',
                         'base_info']

        self.instance = instance
        self.path = path
        self.procedure = procedure
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("cpu")

    @staticmethod
    def read(instance=None):
        """
        instance： 图片对象
        image_content: 二进制文件流
        """
        # 读取图片
        # image_file = self.instance.src.open()  # 方式一：读取本地或网络图片
        if not instance:
            print('instance is None')
            return None
        image_file = default_storage.open(instance.src.name)  # 方式二：读取本地或网络图片
        image_content = image_file.read()
        image_file.close()
        return image_content

    @staticmethod
    def read_img(instance=None, read_type=None):
        """
        instance： 图片对象
        image_content: 二进制文件流
        """
        # 读取图片
        # image_file = self.instance.src.open()  # 方式一：读取本地或网络图片
        if not instance:
            print('instance is None')
            return None
        if read_type is None:
            read_type = ['cv2', 'PIL', 'pyexiv2']
        # print(f"instance.src.name: {instance.src.name}")
        image_file = default_storage.open(instance.src.name)  # 方式二：读取本地或网络图片
        image_content = image_file.read()
        # print(f"image_file: {image_file}")
        # print(f"image_content: {image_content}")
        # print('chardet.detect(image_content)', chardet.detect(image_content)['encoding'])

        image_content_obj = BytesIO(image_content)
        image_file.close()
        image = {
            'cv2': None,
            'PIL': None,
            'pyexiv2': None,
        }
        for type in read_type:
            if type == 'cv2':
                image[type] = cv2.imdecode(np.frombuffer(image_content_obj.getvalue(), np.uint8), cv2.IMREAD_COLOR)
            elif type == 'PIL':
                image[type] = Image.open(image_content_obj)
            elif type == 'pyexiv2':
                # image[type] = pyexiv2.ImageData(image_content)
                try:
                    image[type] = pyexiv2.ImageData(image_content)
                except RuntimeError as e:
                    print(f'ERROR: {e}')
                    image[type] = None
            else:
                raise Exception(f'not support this type: {type}')

        return image

    def save_exif_info(self):
        pass

    @transaction.atomic
    def save_face_instance(self, data):
        """
        实例化的方式进行保存
        """
        # 创建Face对象
        face = Face.objects.create(**data['fc'])

        # 创建FaceLandmarks3D对象列表
        landmarks3d_list = []
        for landmark_data in data['landmarks3d']:
            landmarks3d = FaceLandmarks3D(face=face, x=landmark_data[0], y=landmark_data[1],
                                          z=landmark_data[2])
            landmarks3d_list.append(landmarks3d)
        FaceLandmarks3D.objects.bulk_create(landmarks3d_list)

        # 创建FaceLandmarks2D对象列表
        landmarks2d_list = []
        for landmark_data in data['landmarks2d']:
            landmarks2d = FaceLandmarks2D(face=face, x=landmark_data[0], y=landmark_data[1])
            landmarks2d_list.append(landmarks2d)
        FaceLandmarks2D.objects.bulk_create(landmarks2d_list)

        # 创建Kps对象列表
        kps_list = []
        for kps_data in data['kps']:
            kps = Kps(face=face, x=kps_data[0], y=kps_data[1])
            kps_list.append(kps)
        Kps.objects.bulk_create(kps_list)

        return face

    @transaction.atomic
    def save_face_serializers(self, data):
        """
        序列化的方式进行保存
        """
        face_serializer = FaceSerializer(data=data)
        if face_serializer.is_valid():
            face = face_serializer.save()
            return face
        else:
            raise Exception(face_serializer.errors)

    def face_init(self):
        self.app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=calib['face']['det_threshold'])  # 默认det_thresh=0.5,

    @staticmethod
    def face_crop(image, bbox):
        """
        image: 已经打开的图片数组
        bbox: 人脸框, 格式为[x左上, y左上, wid, height], 单位为像素值
        file：构造后的InMemoryUploadedFile对象
        """

        # 人脸裁剪得到的人脸图像, 其中image是PIL.Image.Image对象
        face_image = image.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
        # face_image.show()

        # 构造 InMemoryUploadedFile 对象
        file_stream = BytesIO()
        face_image.save(file_stream, format='JPEG')
        file_stream.seek(0)

        # 构造人脸图片名字
        face_name = ''.join(random.sample(string.ascii_letters + string.digits, 5)) + '.jpg'  # 随机生成5位字符串作为人脸名字

        # 将文件流的内容读取为字节数据
        file_data = file_stream.getvalue()

        # 构造文件对象
        file = InMemoryUploadedFile(file_stream, None, face_name, 'image/jpeg', len(file_data), None)

        return file

    @staticmethod
    def face_zoom(area, ratio, width, height):  # area: 中心坐标，宽度，高度
        [x, y, w, h] = area

        w = w * ratio
        h = h * ratio
        x1 = max(x - w / 2, 0)
        y1 = max(y - h / 2, 0)
        x2 = min(x1 + w, 1)
        y2 = min(y1 + h, 1)
        # print(f'INFO: the face width is {width}, face height is {height}')
        bbox = [x1 * width, y1 * height, x2 * width, y2 * height]

        return bbox  # 这里的bbox 还是浮点型，后续保存图片的时候统一转换
        # return np.array(bbox).astype(int)

    @staticmethod
    def compute_iou(rec1, rec2):  # 这里的矩形，包括左上角坐标和右下角坐标
        """
        计算两个矩形框的交并比。
        :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
        :param rec2: (x0,y0,x1,y1)
        :return: 交并比IOU.
        """
        # print(f'rec1 is {rec1}, rec2 is {rec2}')
        left_column_max = max(rec1[0], rec2[0])
        right_column_min = min(rec1[2], rec2[2])
        up_row_max = max(rec1[1], rec2[1])
        down_row_min = min(rec1[3], rec2[3])
        # 两矩形无相交区域的情况
        if left_column_max >= right_column_min or down_row_min <= up_row_max:
            return 0
        # 两矩形有相交区域的情况
        else:
            S1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
            S2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
            S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
            return S_cross / (S1 + S2 - S_cross)

    def create_new_profile(self, img_ins, face, face_name):
        img_pil = self.read_img(img_ins, ['PIL']).get('PIL', None)
        bbox = np.round(face.bbox).astype(np.int16)
        username = face_name
        try:
            # 创建一个新用户profile对象，设定默认密码为666，加密保存，User中is_active设置为0， username设置成name，
            # 如果username已经存在相同字段，则在name后面增加4位随机数，再次创建保存
            while Profile.objects.filter(username=username).exists():
                # 生成4位随机数，并与name拼接
                random_suffix = str(random.randint(1000, 9999))
                username = f'{face_name}{random_suffix}'
            print(f'INFO: will created a new profile, the name is : {username}')
        except IntegrityError:
            print('ERROR: Failed to create a new profile. IntegrityError occurred.')

        full_pinyin, lazy_pinyin = get_pinyin(face_name)
        creation_params = {
            'username': username,
            'password': make_password('deep-diary666'),
            'name': face_name,
            'full_pinyin': full_pinyin,
            'lazy_pinyin': lazy_pinyin,
            'avatar': self.face_crop(img_pil, bbox),  # 需要对avatar进行赋值
            'embedding': face.normed_embedding.astype(np.float16).tobytes(),
        }
        profile, created = Profile.objects.get_or_create(name=face_name, defaults=creation_params)
        if created:
            print(f'INFO: success created a new profile: {profile.name}')
        else:
            print(f'INFO: the profile already existed: {profile.name}')

        return profile, created

    @staticmethod
    def img_recognition(text):  # 'instance', serializers

        device = "cuda" if torch.cuda.is_available() else "cpu"
        # device = "cpu"  # 使用cpu 貌似就无法运行
        model, preprocess = clip.load("ViT-B/32", device=device)

        text = clip.tokenize(text).to(device)

        image_features = Img.objects.values_list('embedding', flat=True)
        embeddings = [np.frombuffer(embedding, dtype=np.float32) for embedding in image_features if embedding]
        # 将所有的embedding转换为矩阵形式，大小为N* 512
        embeddings = np.stack(embeddings)

        with torch.no_grad():
            text_features = model.encode_text(text)
            image_features = torch.tensor(embeddings, dtype=torch.float16).to(device)
            # print(text_features.shape)
            # print(image_features.shape)
            # print(type(text_features))
            # print(type(image_features))

        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * text_features @ image_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(5)

        # 方法一: 使用itemgetter根据索引值获取id列表
        # filtered_data = itemgetter(*indices.cpu().numpy().tolist())(imgs)
        # topk_ids = [img.id for img in filtered_data]
        # print('方法一: 使用itemgetter根据索引值获取id列表', topk_ids)

        imgs = Img.objects.all()
        # 方法二: 根据索引值直接获取id列表
        topk_ids = [imgs[i].id for i in indices.cpu().numpy().tolist()]
        # print('方法二: 根据索引值直接获取id列表', topk_ids)

        from django.db.models import Case, When, IntegerField
        # 创建一个排序表达式
        order_by_expression = Case(
            *[
                When(id=id, then=index)  # 每个 id 对应一个索引值
                for index, id in enumerate(topk_ids)
            ],
            default=len(topk_ids),  # 默认情况下，使用 topk_ids 列表的长度作为排序值
            output_field=IntegerField(),
        )
        # 对 imgs 查询集进行排序
        filtered_data = imgs.filter(id__in=topk_ids).order_by(order_by_expression)

        # Print the result
        print("\nTop predictions:\n")
        for value, id in zip(values, topk_ids):
            print(f"{id}: {100 * value.item():.2f}%")

        return filtered_data

    @staticmethod
    def face_recognition(embedding):  # 'instance', serializers
        profile = None
        face_score = 0
        # 1. 提取出Profile模型中所有embedding，记作embeddings，并进行转换
        embeddings = Profile.objects.values_list('embedding', flat=True)
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
            profile = Profile.objects.all()[int(max_similarity_index)]
            face_score = max_similarity_score
            print(f'INFO: recognition result: {profile}--', face_score)
        else:
            # 新创建一个profile
            print(f'INFO: recognition result: unknown--, will create a new profile')

        return profile, face_score

    def face_check_profile(self, img_ins, face, enableLM=True):
        """
        根据人脸检测结果，判断是否需要创建Profile
        img: 图片对象
        face: 人脸识别结果
        names: 通过LightRoom检测到的人脸名字
        bboxs: 通过LightRoom检测到的人脸框
        return:
        profile: Profile对象
        face_score: 人脸相似度
        """

        # 1. 获取人脸名字
        names = []
        bboxs = []
        face_name = 'unknown_' + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        face_score = 0
        if enableLM:  # 通过LM方式检测到了人脸
            names, bboxs = self.get_lm_face_info(img_ins)
        if len(names) > 0:
            ious = []
            for bbox in bboxs:
                iou = self.compute_iou(bbox, face.bbox)  # 计算LM 人脸区域跟insight face 人脸区域的重合度
                ious = np.append(ious, iou)
            idx = ious.argmax()
            print(f'INFO ious is {ious}')
            print(f'INFO names is {names}')
            print(f'INFO: the identified idx is {idx}， ious[idx]: {ious[idx]}')
            if ious[idx] > 0.3:  # 重合度超过30%
                print(f"\033[1;32m INFO: estimated name is {names[idx]}, iou is{ious[idx]} \033[0m")
                face_name = names[idx]
                face_score = 1

            print(f"\033[1;32m INFO: estimated name is {face_name}, which is from LM \033[0m")
            # 检查Profile 数据库中是否包含此人脸名字
            profile, created = self.create_new_profile(img_ins, face, face_name)

        else:  # 通过LM方式未检测到人脸
            print(f'INFO: there is no LM_face_info detected ... ')
            print(f'INFO: estimated face name based on exist feats now  ... ')
            profile, face_score = self.face_recognition(face.normed_embedding)
            if not profile:
                # profile, created = self.create_new_profile(img_ins, face, face_name)
                print(f"\033[1;32m INFO: couldn't find the similar face \033[0m")
            else:
                print(f"\033[1;32m INFO: estimated name is {profile.name}, which is from insightface \033[0m")


        return profile, face_score

    @staticmethod
    def resolve_date(date_str):  # 1. date instance, 2 '%Y:%m:%d %H:%M:%S'
        if not date_str:
            date_str = '1970:01:01 00:00:00'
        tt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        date = {
            'capture_date': tt.strftime("%Y-%m-%d"),
            'capture_time': tt.strftime("%H:%M:%S"),
            'year': str(tt.year).rjust(2, '0'),
            'month': str(tt.month).rjust(2, '0'),
            'day': str(tt.day).rjust(2, '0'),
            'is_weekend': False if tt.weekday() < 5 else True,
            'earthly_branches': bisect.bisect_right(calib['hour_slot'], tt.hour) - 1,
        }
        return date

    @staticmethod
    def profile_category_init():
        # 0. judge whether the profile category have initialized or not
        if Category.objects.filter(name='family').exists():
            return
        # 1. create the root node profile category: [‘家人'，同学'，‘同事’，‘社会朋友’，‘其它公司’]
        root_profile = ['family', 'schoolmate', 'colleague', 'Social friend', 'companies']
        family = ['direct relative', 'relative', 'other']
        schoolmate = ['primary', 'middle', 'high', 'university', 'postgraduate', 'other']

        for name in root_profile:
            name_obj, created = Category.objects.get_or_create(name=name)
            if created:
                dict_name = {
                    'parent': None,
                    'level': 0,
                    'is_leaf': False,
                    'is_root': True,
                    'description': f'this is root_profile: {name}',
                }
                name_obj.__dict__.update(dict_name)
                name_obj.save()
        # 2. create the leaf node profile family: ['direct relative', 'relative', 'other']
        family_instance = Category.objects.get(name='family')
        for name in family:
            name_obj, created = Category.objects.get_or_create(name=name, parent=Category.objects.get(name='family'))
            if created:
                dict_name = {
                    'parent': family_instance,
                    'level': 1,
                    'is_leaf': True,
                    'is_root': False,
                    'description': f'this is family: {name}',
                }
                name_obj.__dict__.update(dict_name)
                name_obj.save()
        # 3. create the leaf node profile schoolmate: ['primary', 'middle', 'high', 'university', 'postgraduate',
        # 'other']
        schoolmate_instance = Category.objects.get(name='schoolmate')
        for name in schoolmate:
            name_obj, created = Category.objects.get_or_create(name=name,
                                                               parent=Category.objects.get(name='schoolmate'))
            if created:
                dict_name = {
                    'parent': schoolmate_instance,
                    'level': 1,
                    'is_leaf': True,
                    'is_root': False,
                    'description': f'this is schoolmate: {name}',
                }
                name_obj.__dict__.update(dict_name)
                name_obj.save()

    @staticmethod
    def category_init():
        # 0. judge whether the profile category have initialized or not
        if Category.objects.filter(name='date').exists():
            return
        # 1. create the root node profile category: [‘家人'，同学'，‘同事’，‘社会朋友’，‘其它公司’]
        root = ['date', 'Holiday', 'location', 'profile', 'event', 'img_color', 'fore_color', 'back_color', 'scene',
                'layout', 'rate', 'group', 'group_num']

        for name in root:
            name_obj, created = Category.objects.get_or_create(name=name)
            if created:
                dict_name = {
                    'parent': None,
                    'level': 0,
                    'is_leaf': False,
                    'is_root': True,
                    'description': f'this is category root: {name}',
                }
                name_obj.__dict__.update(dict_name)
                name_obj.save()

    def __is_need_process__(self, instance=None, force=False, field=None):
        """
        判断是否需要处理
        :param instance: 实例对象
        :param force: 是否强制处理
        :param field: 字段名
        :return: instance: 使用默认实例还是外来实例
        :return: process: 是否需要处理
        """
        process = False
        instance = self.instance if instance is None else instance
        if not hasattr(instance, 'stats'):
            stats, created = Stat.objects.get_or_create(img=instance)  # bind the one to one field image info
        else:
            stats = instance.stats
        if field is not None and hasattr(stats, field):
            value = getattr(stats, field)
            if force:
                print(f'INFO: force stat is {force}')
                process = True
            if not value:
                print(f'INFO: {field} is {value}')
                process = True
        if not process:
            print(
                f'INFO: {field} is True in the Img.stats, that is mean you have already processed this before. however, if you want process this again, you could set the force=True and then try again')
        else:
            print(f'INFO: img-->{instance} is processing {field}, force stat is {force}')
        return instance, stats, process

    def __is_OK_add_to_category__(self, instance=None, force=True, field=None):
        """
        判断是否可以正常加入分类模型
        :param instance: 实例对象
        :param field: 字段名
        """
        process = False
        instance = self.instance if instance is None else instance

        if force:
            print(f'INFO: force stat is {force}')
            process = True
        if not hasattr(instance, field):  # 如果图片没有这个属性，那么就不需要处理
            print(f'INFO: {field} is not existed in the Img')
            process = False
        return instance, process

    #  --------------------process for the single image--------------------
    def get_mcs(self, instance=None, force=False):  # img = self.get_object()  # 获取详情的实例对象

        # 1. 判断是否需要处理
        field = 'is_store_mcs'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        # 2. processing the image
        data = upload_file_pay(cfg['wallet_info'], instance.src.path)
        # 调用序列化器进行反序列化验证和转换
        data.update(id=instance.id)
        print(data)
        serializer = McsDetailSerializer(data=data)
        # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就

        result = serializer.is_valid(raise_exception=True)
        print(serializer.errors)  # 查看错误信息

        # 获取通过验证后的数据
        print(serializer.validated_data)  # form -- clean_data
        # 保存数据
        mcs_obj = serializer.save()

        # 3. update the stats
        stats.is_store_mcs = True
        stats.save()
        print('success to make a copy into mac, the file_upload_id is %d' % mcs_obj.file_upload_id)

    def get_tags(self, instance=None, force=False):
        # 1. 判断是否需要处理
        field = 'is_auto_tag'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        # 2. processing the image

        # img_path = instance.src.path  # oss have no path attribute
        img_path = instance.src.url
        # img_path = 'https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg'
        endpoint = 'tags'
        tagging_query = {
            'verbose': False,
            'language': 'en',
            'threshold': 25,
        }

        # response = imagga_post(img_path, endpoint, tagging_query)  # for local image
        response = imagga_get(img_path, endpoint, query_add=tagging_query)  # for web image

        # with open("tags.txt", 'wb') as f:  # store the result object, which will helpful for debugging
        #     pickle.dump(response, f)
        #
        # with open("tags.txt", 'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
        #     response = pickle.load(f)
        # print(response)

        if 'result' in response:
            tags = response['result']['tags']
            tag_list = []

            for tag in tags:
                tag_list.append(tag['tag']['en'])

            # instance.tags.set(tag_list)
            instance.tags.add(*tag_list)

            # 3. update the stats
            instance.stats.is_auto_tag = True
            instance.stats.save()

            print(f'--------------------{instance.pk} :tags have been store to the database---------------------------')

    # @shared_task
    def get_colors(self, instance=None, force=False):
        # 1. 判断是否需要处理
        field = 'is_get_color'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        # 2. processing the image
        # this is through post method to get the tags. mainly is used for local img
        # img_path = instance.src.path  # local image
        img_path = instance.src.url  # web image
        endpoint = 'colors'
        # color_query = {                 #  if it is necessary, we could add the query info here
        #     'verbose': False,
        #     'language': False,
        #     'threshold': 25.0,
        # # }

        # response = imagga_post(img_path, endpoint)
        response = imagga_get(img_path, endpoint)

        # with open("colors.txt", 'wb') as f:  # store the result object, which will helpful for debugging
        #     pickle.dump(response, f)

        # with open("colors.txt", 'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
        #     response = pickle.load(f)

        # print(response)

        if response['status']['type'] != 'success':
            return []

        if 'result' in response:
            colors = response['result'][endpoint]
            background_colors = colors['background_colors']
            foreground_colors = colors['foreground_colors']
            image_colors = colors['image_colors']

            # print(colors)

            # 调用序列化器进行反序列化验证和转换
            colors.update(img=instance.id)  # bind the one to one field image info
            if not hasattr(instance, 'colors'):  # if instance have no attribute of colors, then create it
                print('no colors object existed')
                serializer = ColorSerializer(data=colors)
            else:  # if instance already have attribute of colors, then updated it
                print('colors object already existed')
                serializer = ColorSerializer(instance.colors, data=colors)
            result = serializer.is_valid(raise_exception=True)
            color_obj = serializer.save()

            # print(type(color_obj))
            # print(color_obj.background.all().exists())
            # print(color_obj.foreground.all().exists())
            # print(color_obj.image.all().exists())

            if not color_obj.background.all().exists():
                for bk in background_colors:
                    bk.update(color=color_obj.pk)
                    serializer = ColorBackgroundSerializer(data=bk)
                    result = serializer.is_valid(raise_exception=True)
                    back_color_obj = serializer.save()
            # else:
            # for bk in background_colors:
            #     bk.update(color=color_obj.pk)
            #     serializer = ColorBackgroundSerializer(color_obj.background, data=bk)
            #     result = serializer.is_valid(raise_exception=True)
            #     back_color_obj = serializer.save()

            if not color_obj.foreground.all().exists():
                for fore in foreground_colors:
                    fore.update(color=color_obj.pk)
                    serializer = ColorForegroundSerializer(data=fore)
                    result = serializer.is_valid(raise_exception=True)
                    fore_color_obj = serializer.save()
            # else:
            #     for fore in foreground_colors:
            #         fore.update(color=color_obj.pk)
            #         serializer = ColorForegroundSerializer(color_obj.foreground, data=fore)
            #         result = serializer.is_valid(raise_exception=True)
            #         fore_color_obj = serializer.save()

            if not color_obj.image.all().exists():
                for img in image_colors:
                    img.update(color=color_obj.pk)
                    serializer = ColorImgSerializer(data=img)
                    result = serializer.is_valid(raise_exception=True)
                    img_color_obj = serializer.save()
            # else:
            #     for img in image_colors:
            #         img.update(color=color_obj.pk)
            #         serializer = ColorImgSerializer(color_obj.image, data=img)
            #         result = serializer.is_valid(raise_exception=True)
            #         img_color_obj = serializer.save()

            # 3. update the stats
            instance.stats.is_get_color = True
            instance.stats.save()
            print(
                f'--------------------{instance.id} :colors have been store to the database---------------------------')

    # @shared_task
    def get_categories(self, instance=None, force=False):
        # 1. 判断是否需要处理
        field = 'is_get_cate'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        # 2. processing the image
        # img_path = instance.src.path  # local image
        img_path = instance.src.url  # web image
        endpoint = 'categories/personal_photos'

        # response = imagga_post(img_path, endpoint)
        response = imagga_get(img_path, endpoint)
        # with open("categories.txt", 'wb') as f:  # store the result object, which will helpful for debugging
        #     pickle.dump(response, f)

        # with open("categories.txt",
        #           'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
        #     response = pickle.load(f)
        # print(response)

        if 'result' in response:
            categories = response['result']['categories']
            categories_list = []
            img_cate_list = []
            data = {}

            for item in categories:
                field_list = [
                    'scene',
                    item['name']['en'],
                ]
                self.__add_levels_to_category__(instance=instance,
                                                field_list=field_list)
            #     # obj = Category(name=item['name']['en'], confidence=item['confidence'])
            #     checkd_obj = Category.objects.filter(name=item['name']['en'])
            #     if checkd_obj.exists():
            #         # print(f'--------------------categories have already existed---------------------------')
            #         # return
            #         obj = checkd_obj.first()
            #     else:
            #         obj = Category.objects.create(name=item['name']['en'])
            #
            #     if ImgCategory.objects.filter(img=instance, category=obj).exists():
            #         print(f'--------------------ImgCategory have already existed---------------------------')
            #         continue
            #     item = ImgCategory(img=instance, category=obj, confidence=item['confidence'])
            #     img_cate_list.append(item)
            #     categories_list.append(obj)
            #
            # ImgCategory.objects.bulk_create(img_cate_list)

            # instance.categories.add(*categories_list, through_defaults=confidence_list)
            # 3. update the stats
            instance.stats.is_get_cate = True
            instance.stats.save()
            print(
                f'--------------------{instance.id} :categories have been store to the database---------------------------')

    def get_clip_classification(self, instance=None, force=False, cls_names=None):
        # 1. 判断是否需要处理
        field = 'is_get_clip_classification'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return

        if cls_names is None:
            #  classification
            cls_names = [
                "interior objects",
                "nature landscape",
                "beaches seaside",
                "events parties",
                "food drinks",
                "paintings art",
                "pets animals",
                "text visuals",
                "sunrises sunsets",
                "cars vehicles",
                "macro flowers",
                "streetview architecture",
                "people portraits",
            ]
        # 2. processing the image
        categories = []

        raw_image = self.read_img(instance, ['PIL']).get('PIL', None).convert("RGB")
        # Load CLIP feature extractor model,
        # vis_processors, txt_processors = load_model_and_preprocess(
        # "clip_feature_extractor", model_type="ViT-B-32", is_eval=True, device=device)
        model, vis_processors, txt_processors = load_model_and_preprocess("clip_feature_extractor",
                                                                          model_type="ViT-B-32", is_eval=True,
                                                                          device=self.device)
        # Optional to use prompts to guide the model
        cls_names = [txt_processors["eval"](cls_nm) for cls_nm in cls_names]

        image = vis_processors["eval"](raw_image).unsqueeze(0).to(self.device)
        #  Extract image embedding and class name embeddings
        sample = {"image": image, "text_input": cls_names}
        clip_features = model.extract_features(sample)
        image_features = clip_features.image_embeds_proj
        text_features = clip_features.text_embeds_proj

        # Matching image embeddings with each class name embeddings
        sims = (image_features @ text_features.t())[0] / 0.01
        probs = torch.nn.Softmax(dim=0)(sims).tolist()

        prob_max = max(probs)
        cla_name = cls_names[probs.index(prob_max)]
        for cls_nm, prob in zip(cls_names, probs):
            if prob > 0.25:
                print(f"{cls_nm}: \t {prob:.3%}")
                # 3. save the result
                field_list = [
                    'clip_categories',
                    cls_nm,
                ]
                self.__add_levels_to_category__(instance=instance,
                                                field_list=field_list)

        # 4. update the stats
        stats.is_get_clip_classification = True
        stats.save()
        print(
            f'--------------------{instance.id} : clip categories have been store to the database---------------------------')

    def get_date(self, instance, img_pyexiv2=None, img_pil=None):
        print(f'INFO: -------------------start getting date info for img id {instance.id}--------------------')
        # through pyexiv2 method
        # img_read = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)
        try:
            exif = img_pyexiv2.read_exif()  # 读取元数据，这会返回一个字典
        except (AttributeError,UnicodeDecodeError) as e:
            print(f'INFO: get_date----->UnicodeDecodeError {e} ')
            exif = None

        if exif:
            print(f'INFO: get_date----->exif is true ')
            # deal with timing
            date_str = exif.get('Exif.Photo.DateTimeOriginal', '1970:01:01 00:00:00')
        else:
            date_str = '1970:01:01 00:00:00'
        date_dict = self.resolve_date(date_str)  # return the date instance
        print(f'INFO: -------------------finish getting date info for img id {instance.id}--------------------')
        return date_dict

    def get_addr(self, instance, img_pyexiv2=None, img_pil=None):
        print(f'INFO: -------------------start getting address info for img id {instance.id}--------------------')

        addr = {}
        # img_read = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)

        try:
            exif = img_pyexiv2.read_exif()  # 读取元数据，这会返回一个字典
        except (AttributeError, UnicodeDecodeError) as e:
            print(f'INFO: get_addr----->UnicodeDecodeError {e} ')
            exif = None

        if exif:
            print(f'INFO: get_addr----->exif is true ')

            longitude = GPS_format(exif.get('Exif.GPSInfo.GPSLongitude'), )
            latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude'))
            altitude = exif.get('Exif.GPSInfo.GPSAltitude')  # 根据高度信息，最终解析成float 格式
            if type(altitude) == str:
                alt = altitude.split('/')
                altitude = float(alt[0]) / float(alt[1])

            is_located = True if longitude and latitude else False

            long_lati = None
            if is_located:
                long_lati = GPS_to_coordinate(longitude, latitude)
                # TODO: need update the lnglat after transform the GPS info
                longitude = round(long_lati[0], 6)  # only have Only 6 digits of precision for AMAP
                latitude = round(long_lati[1], 6)
                # print(f'instance.longitude {addr.longitude},instance.latitude {addr.latitude}')
                long_lati = f'{long_lati[0]},{long_lati[1]}'  # change to string
                print(f'INFO: get_addr----->long_lati is {long_lati}')

            location, district, city, province, country = GPS_get_address(long_lati)

            addr = {
                'longitude_ref': exif.get('Exif.GPSInfo.GPSLongitudeRef', 'E'),
                'longitude': longitude,
                'latitude_ref': exif.get('Exif.GPSInfo.GPSLatitudeRef', 'N'),
                'latitude': latitude,
                'altitude_ref': float(exif.get('Exif.GPSInfo.GPSAltitudeRef', 0.0)),
                'altitude': altitude,
                'is_located': is_located,
                'country': country,
                'province': province,
                'city': city,
                'district': district,
                'location': location,
            }
        else:
            # other method to get the addr info
            print(f'INFO: get_addr----->exif is false ')
        print(f'INFO: -------------------finish getting address info for img id {instance.id}--------------------')
        return addr

    def get_eval(self, instance, img_pyexiv2=None, img_pil=None):
        print(f'INFO: -------------------start getting eval info for img id {instance.id}--------------------')
        # img_read = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)

        xmp = img_pyexiv2.read_xmp()  # 读取元数据，这会返回一个字典
        rating = int(xmp.get('Xmp.xmp.Rating', 0))
        rate = {
            'rating': rating,
        }
        print(f'INFO: -------------------finish getting eval info for img id {instance.id}--------------------')
        return rate

    def get_base(self, instance, img_pyexiv2=None, img_pil=None):  # 传入img_pyexiv2和img_pil为了降低读取图片的次数，提高效率
        print(f'INFO: -------------------start getting base info for img id {instance.id}--------------------')
        # img_pyexiv2 = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)
        # img_pil = self.read_img(instance, ['PIL']).get('PIL', None)

        # # # 获取属性列表
        # img_attributes = dir(img_pil)
        # # # 遍历属性并打印
        # for attr in img_attributes:
        #     attr_value = getattr(img_pil, attr)
        #     print(f"Attribute: {attr}, Value: {attr_value}")

        try:
            exif = img_pyexiv2.read_exif()  # 读取元数据，这会返回一个字典
        except (AttributeError, UnicodeDecodeError) as e:
            print(f'INFO: get_base----->UnicodeDecodeError {e} ')
            exif = None
        # exif = img_pyexiv2.read_exif()  # 读取元数据，这会返回一个字典
        iptc = img_pyexiv2.read_iptc()  # 读取元数据，这会返回一个字典
        xmp = img_pyexiv2.read_xmp()  # 读取元数据，这会返回一个字典
        # print(f'INFO: exif is {json.dumps(exif, indent=4)}')
        # print(f'INFO: iptc is {json.dumps(iptc, indent=4)}')
        # print(f'INFO: xmp is {json.dumps(xmp, indent=4)}')

        wid = int(exif.get('Exif.Image.ImageWidth', 0)) if exif and int(exif.get('Exif.Image.ImageWidth', 0)) else int(
            img_pil.width)  # 其实本身已经是int类型的了
        height = int(exif.get('Exif.Image.ImageLength', 0)) if exif and int(
            exif.get('Exif.Image.ImageLength', 0)) else int(img_pil.height)  # 其实本身已经是int类型的了
        print(wid, height)
        aspect_ratio = height / wid if wid != 0 else 0
        camera_brand = exif.get('Exif.Image.Make', '') if exif else ''
        camera_model = exif.get('Exif.Image.Model', '') if exif else ''

        title = iptc.get('iptc.Application2.ObjectName') if iptc else ''
        caption = iptc.get('Iptc.Application2.Caption') if iptc else ''
        lm_tags = iptc.get('Iptc.Application2.Keywords') if iptc else []

        label = xmp.get('Xmp.xmp.Label') if xmp else ''

        base = {
            'wid': wid,
            'height': height,
            'aspect_ratio': aspect_ratio,
            'camera_brand': camera_brand,
            'camera_model': camera_model,
            'title': title,
            'caption': caption,
            'label': label,
            'is_exist': True,
        }
        print(f'INFO: -------------------finish getting base info for img id {instance.id}--------------------')
        return base, lm_tags

    def get_exif_info(self, instance=None, force=False):

        # 1. 判断是否需要处理
        field = 'is_get_info'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return
        img = self.read_img(instance, ['pyexiv2', 'PIL'])
        img_pyexiv2 = img.get('pyexiv2', None)
        img_pil = img.get('PIL', None)

        # img_pyexiv2 = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)
        # img_pil = self.read_img(instance, ['PIL']).get('PIL', None)

        if not img_pyexiv2 or not img_pil:
            return

        # 2. processing the image
        print(f'INFO: --------------------start dealing with get_exif_info------------')
        # stat, created = Stat.objects.get_or_create(img=instance)  # bind the one to one field image info
        addr, created = Address.objects.get_or_create(img=instance)
        eval, created = Evaluate.objects.get_or_create(img=instance)
        date, created = Date.objects.get_or_create(img=instance)

        date_dict = self.get_date(instance, img_pyexiv2=img_pyexiv2, img_pil=img_pil)
        date.__dict__.update(date_dict)
        date.save()

        addr_dict = self.get_addr(instance, img_pyexiv2=img_pyexiv2, img_pil=img_pil)
        addr.__dict__.update(addr_dict)
        addr.save()

        eval_dict = self.get_eval(instance, img_pyexiv2=img_pyexiv2, img_pil=img_pil)
        eval.__dict__.update(eval_dict)
        eval.save()

        base_dict, lm_tags = self.get_base(instance, img_pyexiv2=img_pyexiv2, img_pil=img_pil)
        instance.__dict__.update(base_dict)
        instance.save()

        print(lm_tags)

        if lm_tags:
            instance.tags.add(*lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
        print(f'INFO: --------------------finish dealing with get_exif_info------------')

        # 3. update the stats
        stats.is_publish = True
        stats.is_get_info = True

        stats.save()

        # if exif:
        #     print(f'INFO: exif is true ')
        #     # deal with timing
        #     date_str = exif['Exif.Photo.DateTimeOriginal']
        #
        #     # date = set_img_date(date, date_str)  # return the date instance
        #     date_dict = self.resolve_date(date_str)  # return the date instance
        #     date.__dict__.update(date_dict)
        #
        #     # deal with address
        #     addr.longitude_ref = exif.get('Exif.GPSInfo.GPSLongitudeRef')
        #     if addr.longitude_ref:  # if have longitude info
        #         addr.longitude = GPS_format(
        #             exif.get('Exif.GPSInfo.GPSLongitude'))  # exif.get('Exif.GPSInfo.GPSLongitude')
        #         addr.latitude_ref = exif.get('Exif.GPSInfo.GPSLatitudeRef')
        #         addr.latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude'))
        #
        #     addr.altitude_ref = exif.get('Exif.GPSInfo.GPSAltitudeRef')  # 有些照片无高度信息
        #     if addr.altitude_ref:  # if have the altitude info
        #         addr.altitude_ref = float(addr.altitude_ref)
        #         addr.altitude = exif.get('Exif.GPSInfo.GPSAltitude')  # 根据高度信息，最终解析成float 格式
        #         alt = addr.altitude.split('/')
        #         addr.altitude = float(alt[0]) / float(alt[1])
        #     addr.is_located = False
        #     if addr.longitude and addr.latitude:
        #         # 是否包含经纬度数据
        #         addr.is_located = True
        #         long_lati = GPS_to_coordinate(addr.longitude, addr.latitude)
        #         # TODO: need update the lnglat after transform the GPS info
        #         addr.longitude = round(long_lati[0], 6)  # only have Only 6 digits of precision for AMAP
        #         addr.latitude = round(long_lati[1], 6)
        #         # print(f'instance.longitude {addr.longitude},instance.latitude {addr.latitude}')
        #         long_lati = f'{long_lati[0]},{long_lati[1]}'  # change to string
        #
        #         addr.location, addr.district, addr.city, addr.province, addr.country = GPS_get_address(
        #             long_lati)
        #
        #     instance.wid = int(exif.get('Exif.Image.ImageWidth'), 0)
        #     instance.height = int(exif.get('Exif.Image.ImageLength'), 0)
        #     if instance.wid and instance.height:
        #         instance.aspect_ratio = instance.height / instance.wid
        #     instance.camera_brand = exif.get('Exif.Image.Make')
        #     instance.camera_model = exif.get('Exif.Image.Model')
        # else:
        #     # print(f'INFO: exif is false ')
        #     # # 2.2 get the exif info by PIL
        #     img_pil = self.read_img(instance, ['PIL']).get('PIL', None)
        #     # # 获取属性列表
        #     img_attributes = dir(img_pil)
        #     #
        #     # # 遍历属性并打印
        #     for attr in img_attributes:
        #         attr_value = getattr(img_pil, attr)
        #         print(f"Attribute: {attr}, Value: {attr_value}")
        #     # print(type(img_pil.width))  # int 类型
        #     instance.wid = int(img_pil.width)  # 其实本身已经是int类型的了
        #     instance.height = int(img_pil.height)  # 其实本身已经是int类型的了
        #     instance.aspect_ratio = instance.height / instance.wid
        #
        # if iptc:
        #     # print(f'INFO: iptc is true ')
        #     instance.title = iptc.get('iptc.Application2.ObjectName')
        #     instance.caption = iptc.get('Iptc.Application2.Caption')  # Exif.Image.ImageDescription
        #     lm_tags = iptc.get('Iptc.Application2.Keywords')
        # else:
        #     # print(f'INFO: iptc is false ')
        #     pass
        #
        # if xmp:
        #     # print(f'INFO: xmp is true ')
        #     instance.label = xmp.get('Xmp.xmp.Label')  # color mark
        #     eval.rating = int(xmp.get('Xmp.xmp.Rating', 0))
        #     # if eval.rating:
        #     #     eval.rating = int(xmp.get('Xmp.xmp.Rating'))
        #
        # else:
        #     # print(f'INFO: xmp is false ')
        #     pass
        #
        # # 使用阿里云后端，这个无法直接访问
        # # instance.wid = instance.src.width
        # # instance.height = instance.src.height
        # # instance.aspect_ratio = instance.height / instance.wid
        # instance.is_exist = True
        # instance.save()  # save the image instance, already saved during save the author
        #
        # if lm_tags:
        #     # print(f'INFO: the lm_tags is {lm_tags}, type is {type(lm_tags)}')
        #     # print(f'INFO: the instance id is {instance.id}')
        #     # instance.tags.set(lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
        #     instance.tags.add(*lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
        #
        # # 3. update the stats
        # stats.is_publish = True
        # stats.is_get_info = True
        #
        # addr.save()
        # eval.save()
        # date.save()
        # stats.save()
        # print(
        #     f'--------------------{instance.id} :img infos have been store to the database---------------------------')

    def get_lm_face_info(self, instance):
        print(f'INFO: get_LM_face_info ... ')
        num = 1  # xmp 内容下表从1开始
        is_have_face = True
        names = []
        bboxs = []
        # img_read = pyexiv2.ImageData(self.read(instance))  # 登记图片路径
        img = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)
        if img is None:
            print(f'INFO: img is None')
            return names, bboxs
        xmp = img.read_xmp()  # 读取元数据，这会返回一个字典
        # print(f'INFO: xmp is {json.dumps(xmp, indent=4)}')
        while is_have_face:
            item = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Type'.format(num)
            is_have_face = xmp.get(item, None)
            if is_have_face:
                print(f'INFO: LM face detected')
                idx_name = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Name'.format(num)
                idx_h = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:h'.format(num)
                idx_w = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:w'.format(num)
                idx_x = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:x'.format(num)
                idx_y = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:y'.format(num)
                num += 1

                name = xmp.get(idx_name, 'unknown')
                names.append(name)
                lm_face_area = [xmp.get(idx_x), xmp.get(idx_y), xmp.get(idx_w), xmp.get(idx_h)]  # 0~1 之间的字符
                lm_face_area = np.array(lm_face_area).astype(float)  # 0~1 之间的浮点，中心区域，人脸长，宽
                # bbox = face_zoom(lm_face_area, 1, instance.src.width, instance.src.height)  # 转变成像素值，左上区域和右下区域坐标，跟insightface 保持一致
                bbox = self.face_zoom(lm_face_area, 1, instance.wid,
                                      instance.height)  # 转变成像素值，左上区域和右下区域坐标，跟insightface 保持一致
                bboxs.append(bbox)
        # print(f'INFO: the LM names is {names}, bbox is {bboxs}')
        return names, bboxs

    def get_faces(self, instance=None, force=False, save_type='instance'):  # 'instance', serializers
        #  判断当前实例是否已经执行过人脸识别，如果是，直接打印相关信息并返回
        # 1. 判断是否需要处理
        field = 'is_face'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return
        print(f'INFO: start get_faces ... the img id is : {instance.id}------------------------------')
        # 1.1 delete the old faces and relations to Profile
        if stats.is_face:
            print(f'INFO: the instance {instance.id} has been processed')
            # 清除Img与Profile之间的多对多关系
            instance.profiles.clear()
            # 清除Img与Profile之间的多对多关系
            instance.faces.all().delete()

        # 2. processing the image
        self.face_init()
        # image_content = self.read(instance)
        # image_content_obj = BytesIO(image_content)
        # 
        # np_array = np.frombuffer(image_content_obj.getvalue(), np.uint8)
        # image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        # img_pil = Image.open(image_content_obj)

        img = self.read_img(instance, ['cv2', 'PIL'])
        img_cv2 = img.get('cv2', None)
        img_pil = img.get('PIL', None)

        faces = self.app.get(img_cv2)
        print(f'INFO: get_faces ... the img id is : {instance.id}, total face numbers is {len(faces)}------------------------------')

        for face in faces:
            pose = face.pose.astype(np.float16)
            bbox = np.round(face.bbox).astype(np.int16)
            # 人脸识别---->profile
            # 检查是否存在profile对象，如果不存在，则创建profile对象
            # profile, face_score = self.face_recognition(face.normed_embedding)
            profile, face_score = self.face_check_profile(instance, face)

            if save_type == 'instance':
                fc = {
                    'img': instance,
                    'profile': profile,
                    'det_score': face.det_score,
                    'face_score': face_score,
                    'is_confirmed': True if face_score > 0.8 else False,
                    'src': self.face_crop(img_pil, bbox),  # 需要对src进行赋值
                    'age': face.age,
                    'gender': face.gender,
                    'embedding': face.normed_embedding.astype(np.float16).tobytes(),
                    'pose_x': pose[0],
                    'pose_y': pose[1],
                    'pose_z': pose[2],
                    'x': bbox[0],
                    'y': bbox[1],
                    'wid': bbox[2] - bbox[0],
                    'height': bbox[3] - bbox[1],
                }
                data = {
                    'fc': fc,
                    'kps': np.round(face.kps).astype(np.int16),
                    'landmarks2d': np.round(face.landmark_2d_106).astype(np.int16),
                    'landmarks3d': np.round(face.landmark_3d_68).astype(np.int16),
                }
                self.save_face_instance(data)
            if save_type == 'serializers':
                data = {
                    'img': self.instance.id,
                    'det_score': face.det_score,
                    'age': face.age,
                    'gender': face.gender,
                    'embedding': face.normed_embedding.astype(np.float16).tobytes(),
                    'pose_x': pose[0],
                    'pose_y': pose[1],
                    'pose_z': pose[2],
                    'x': bbox[0],
                    'y': bbox[1],
                    'wid': bbox[2],
                    'height': bbox[3],
                    'kps': [{"x": item[0], "y": item[1]} for item in np.round(face.kps).astype(np.int16)],
                    'landmarks2d': [{"x": item[0], "y": item[1]} for item in
                                    np.round(face.landmark_2d_106).astype(np.int16)],
                    'landmarks3d': [{"x": item[0], "y": item[1], "z": item[2]} for item in
                                    np.round(face.landmark_3d_68).astype(np.int16)],
                }
                self.save_face_serializers(data)

            # 如果profile 存在，则将外键asserts中的face_cnt+1
            # process = ProfileProcess()
            # process.get_asserts(instance=profile)
            ProfileProcess.get_asserts(instance=profile)
            # if profile:
            #     # 查找或创建asserts对象
            #     asserts, created = Assert.objects.get_or_create(profile=profile)
            #     # 将外键asserts中的face_cnt+
            #     # asserts.face_cnt = F('face_cnt')+1
            #     # asserts.img_cnt = F('img_cnt')+1
            #     asserts.face_cnt = profile.faces.count()
            #     asserts.img_cnt = profile.imgs.count()
            #     asserts.save()

        # 3. update the stats
        stats.is_face = True
        stats.save()
        return faces

    def get_caption(self, instance=None, force=False):  # 'instance', serializers
        """
        purpose: 对图片进行简单描述
        params:
            instance: the image django instance
            force: identify whether you need to process this instance even this instance already processed
        return:
            caption: the caption of the image
        """
        # 1. 判断是否需要处理
        field = 'is_get_caption'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return
        device = self.device
        raw_image = self.read_img(instance, ['PIL']).get('PIL', None)
        raw_image = raw_image.convert("RGB")
        # loads BLIP caption base model, with finetuned checkpoints on MSCOCO captioning dataset.
        # this also loads the associated image processors
        model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True,
                                                             device=device)
        # preprocess the image
        # vis_processors stores image transforms for "train" and "eval" (validation / testing / inference)
        image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
        # generate caption
        caption = model.generate({"image": image})
        print(caption)

        # save the caption to the database
        instance.caption = ''.join(caption)  # 将列表转成字符串
        instance.save()

        # update the stat
        stats.is_get_caption = True
        stats.save()

        return caption

    def get_feature(self, instance=None, force=False):  # 'instance', serializers
        """
        purpose: get the feature of the image
        params:
            instance: the image django instance
        return:
            feature: the feature of the image
        """
        # 1. 判断是否需要处理
        field = 'is_get_feature'
        instance, stats, process = self.__is_need_process__(instance, force, field)
        if not process:
            return
        device = self.device
        raw_image = self.read_img(instance, ['PIL']).get('PIL', None)
        model, preprocess = clip.load("ViT-B/32", device=device)
        image = preprocess(raw_image).unsqueeze(0).to(device)

        # caption = self.get_caption(instance)
        # caption.append('a boy is running on the ground')
        # print(caption)
        # text = clip.tokenize(caption).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            print("Image features:", image_features.shape)
            # text_features = model.encode_text(text)
            # print("Text features:", text_features.shape)

        #     logits_per_image, logits_per_text = model(image, text)
        #     probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        # print("Label probs:", probs)

        # save the feature to the database
        instance.embedding = image_features.cpu().numpy().tobytes()
        instance.save()
        # update the stat
        stats.is_get_feature = True
        stats.save()

        return image_features

    # ----------------------process for single img for several functions----------------------
    @shared_task
    def get_img(self, instance=None, func_list=None, force=False):
        """
        :param instance: the instance of the image
        :param func_list: the list of the function
        :param force: if force is True, then the function will be executed
        the function list could be as follows:
        func_list = ['get_mcs', 'get_tags', 'get_colors', 'get_categories', 'get_exif_info', 'get_faces']
        get_mcs(self, instance=None, force=False)
        get_tags(self, instance=None, force=False)
        get_colors(self, instance=None, force=False)
        get_categories(self, instance=None, force=False)
        get_exif_info(self, instance=None, force=False)
        get_faces(self, instance=None, force=False)
        :return:
        """
        print(
            f'-------------INFO: start loop the  funcs, dealing with img --->{instance.id}, func_list is {func_list}---------------')
        if func_list is None:
            func_list = cfg["img"]["process_list"]
        # 1. get the instance
        instance = self.instance if instance is None else instance
        # 2. loop the function list
        for func_name in func_list:
            print(f'-------------INFO: This is func: {func_name} , dealing with img --->{instance.id}---------------')
            func = getattr(self, func_name, None)
            if func is None:
                print(
                    f'-------------INFO: there is no func: {func_name} , dealing with img --->{instance.id}---------------')
                continue
            func(instance=instance, force=force)

    #  ----------------------process for all the imgs for several functions----------------------
    @shared_task
    def get_all_img(self, func_list=None, force=False):
        """
        :param func_list: the list of the function
        :param force: if force is True, then the function will be executed
        the function list could be as follows:
        func_list = ['get_mcs', 'get_tags', 'get_colors', 'get_categories', 'get_exif_info', 'get_faces']
        get_mcs(self, instance=None, force=False)
        get_tags(self, instance=None, force=False)
        get_colors(self, instance=None, force=False)
        get_categories(self, instance=None, force=False)
        get_exif_info(self, instance=None, force=False)
        get_faces(self, instance=None, force=False)
        :return:
        """
        if func_list is None:
            return
        # 1. get all the imgs
        imgs = Img.objects.filter(stats__is_deleted=False)
        # 2. Go through each img
        for (img_idx, img) in enumerate(imgs):
            print(f'--------------------INFO: This is img{img_idx}: {img.id} ---------------------')

            self.get_img(self, instance=img, func_list=func_list, force=force)

    # ----------------------add the single image to category----------------------

    # TODO: 按json格式添加分类
    # def __add_json_to_tree__(self, parent_item, json_data):
    #     # 递归添加 JSON 数据到树形视图中
    #     if isinstance(json_data, dict):
    #         for key, value in json_data.items():
    #             item = QStandardItem(key)
    #             parent_item.appendRow(item)
    #             self.add_json_to_tree(item, value)
    #     elif isinstance(json_data, list):
    #         for item in json_data:
    #             child_item = QStandardItem()
    #             parent_item.appendRow(child_item)
    #             self.add_json_to_tree(child_item, item)
    #     else:
    #         item = QStandardItem(str(json_data))
    #         parent_item.appendRow(item)

    def __add_levels_to_category__(self, instance=None, field_list=None, force=True):

        """
        add the levels to the category
        :param instance: the instance of the image
        :param field_list: the list of the field, the first item is the level 0, then the level 1, level 2, level 3
        :return: category instance
        """
        levels = len(field_list)
        if not levels:
            print(f'INFO: there is no field_list')
            return

        parent_obj = None

        # 2. check the root category is existed or not, if not, create it
        # parent_obj, created = Category.objects.get_or_create(name=field_list[0], defaults=creation_params)
        # 3. loop the field_list
        print(f'INFO: the field_list is {field_list}, will be added to the category')
        for (idx, field) in enumerate(field_list):
            # if idx == 0:  # skip the first item
            #     continue
            creation_params = {
                'level': idx,
                'is_leaf': True if idx == levels - 1 else False,
                'is_root': True if idx == 0 else False,
                'owner': instance.user,
                'avatar': instance.src,
                'description': f'this is {field} category',
                'parent': None if idx == 0 else parent_obj,
            }
            get_params = {
                'parent': None if idx == 0 else parent_obj,
                'name': field,
            }
            category_obj, created = Category.objects.get_or_create(**get_params, defaults=creation_params)
            # category_obj, created = Category.objects.get_or_create(name=field, defaults=creation_params)
            # add the instance to the category
            category_obj.imgs.add(instance)
            parent_obj = category_obj
        return parent_obj

    def add_date_to_category(self, instance=None):
        # 1. get the instance and check is it OK to add to category
        instance, process = self.__is_OK_add_to_category__(instance=instance, field='dates')
        if not process:
            return
        # 2. get the date
        dates = instance.dates
        # 使用模型字段值构建日期对象
        # print(type(dates.year), type(dates.month), type(dates.day))
        date_obj = datetime(int(dates.year), int(dates.month), int(dates.day))
        field_list = [
            'date',
            date_obj.year,
            f'{date_obj.year:02d}-{date_obj.month:02d}',
            f'{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d}',
        ]
        self.__add_levels_to_category__(instance=instance,
                                        field_list=field_list)

    def add_location_to_category(self, instance=None):
        # 1. get the instance and check if it is OK to add to the category
        instance, process = self.__is_OK_add_to_category__(instance=instance, field='address')
        if not process:
            return
        # 2. get the location
        location = instance.address
        field_list = [
            'location',
            location.country if location.country and location.country != '[]' else 'No GPS',
            location.province if location.province and location.province != '[]' else 'No GPS',
            location.city if location.city and location.city != '[]' else 'No GPS',
            location.district if location.district and location.district != '[]' else 'No GPS',
        ]
        self.__add_levels_to_category__(instance=instance,
                                        field_list=field_list)

    def add_profile_to_category(self, instance=None):
        # 1. get the instance and check is it OK to add to category
        instance, process = self.__is_OK_add_to_category__(instance=instance, field='profiles')
        if not process:
            return
        # 2. get the profiles
        profiles = instance.profiles.all()
        # check the profile root is existed or not
        profile_root_obj, created = Category.objects.get_or_create(name='profile')
        # deal with something if this is the first time to create the root
        if created:
            dict_root = {
                'parent': None,
                'level': 0,
                'is_leaf': False,
                'is_root': True,
                'owner': instance.user,
                'avatar': instance.src,
                'description': 'this is profile category',
            }
            profile_root_obj.__dict__.update(dict_root)
            profile_root_obj.save()

        # 3. check whether the profile.name is existed or not, if not, create it
        for profile in profiles:
            name_obj, created = Category.objects.get_or_create(name=profile.name)
            # 4. deal with something if this is the first time to create the name
            if created:
                dict_name = {
                    'parent': None,
                    'level': 2,
                    'is_leaf': True,
                    'is_root': False,
                    'owner': instance.user,
                    'avatar': instance.src,
                    'description': f'this is profile name: {profile.name}',
                }
                name_obj.__dict__.update(dict_name)
                name_obj.save()
            # 5. add the instance to the name
            name_obj.imgs.add(instance)

    def add_group_to_category(self, instance=None):

        # 1. get the instance and check is it OK to add to category
        instance, process = self.__is_OK_add_to_category__(instance=instance, field='profiles')
        if not process:
            return

        # 2. get the profiles in this instance
        names = instance.profiles.order_by('name').values_list('name', flat=True)
        name_cnt = names.count()
        name_str = 'no face'  # default
        if name_cnt <= 1:
            # print(
            #     f'----------------{instance.id} :return-->this is the single or no face-----------------------')
            return
        elif name_cnt <= 5:  # if faces biger then 1, small then 6
            # print(
            # f'----------------{instance.id} :found the face group-----------------------')
            name_str = ' '.join(names)
        elif name_cnt:  # if faces biger then 5, then break
            # print(
            #     f'----------------{instance.id} :too many faces in the img-----------------------')
            name_str = 'group face'

        field_list = [
            'group',
            name_str
        ]

        self.__add_levels_to_category__(instance=instance,
                                        field_list=field_list)

    def add_colors_to_category(self, instance=None):
        # 1. get the instance and check if it is OK to add to the category
        instance, process = self.__is_OK_add_to_category__(instance=instance, field='colors')
        if not process:
            return
        # 2. get the colors
        img_colors = instance.colors.image.all()
        for color in img_colors:
            field_list = [
                'img_color',
                # color_palette[color.closest_palette_color_parent]
                color.closest_palette_color_parent
            ]
            self.__add_levels_to_category__(instance=instance, field_list=field_list)

    def add_layout_to_category(self, instance=None):

        # 2. get the layout
        if instance.aspect_ratio == 1:
            layout = 'Square'
        elif instance.aspect_ratio < 1:
            layout = 'Wide'
        else:
            layout = 'Tall'

        field_list = [
            'layout',
            layout
        ]
        self.__add_levels_to_category__(instance=instance, field_list=field_list)

    def add_size_to_category(self, instance=None):

        # 2. get the layout
        len = max(instance.wid, instance.height)
        if len < 512:
            size = 'Small'
        elif len < 1024:
            size = 'Medium'
        elif len < 2048:
            size = 'Large'
        else:
            size = 'Extra large'
        field_list = [
            'size',
            size
        ]
        self.__add_levels_to_category__(instance=instance, field_list=field_list)

    # ----------------------add the single img to category for several types----------------------
    @shared_task
    def add_img_to_category(self, instance=None, func_list=None):
        """
                :param instance: the instance of the image
                :param func_list: the list of what need to add to the category
                the function list could be as follows:
                func_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category', 'add_colors_to_category']
                :return:
                """
        if func_list is None:
            func_list = cfg["img"]["add_list"]
        # 1. get the instance
        instance = self.instance if instance is None else instance
        # 2. loop the function list
        for func_name in func_list:
            print(f'--------------------INFO: This is func: {func_name} ---------------------')
            # if func_name ==‘’ 或者None, 则跳过
            if not func_name:
                continue
            func = getattr(self, func_name)
            func(instance=instance)

    # ----------------------add the all images to category for several types----------------------
    @shared_task
    def add_all_img_to_category(self, func_list=None, force=False):
        if func_list is None:
            return
        # 1. get all the imgs
        imgs = Img.objects.all()
        # 2. Go through each img
        for (img_idx, img) in enumerate(imgs):
            print(f'--------------------INFO: This is img_{img.id}, current img cnt is: {img_idx}---------------------')
            self.add_img_to_category(self, instance=img, func_list=func_list)

    # ----------------------some functions----------------------

    @staticmethod
    def face_rename(fc_instance, name=None):  # 'instance', serializers
        """
        fc_instance: Face 实例对象
        name：api请求的名字
        """
        # 如果没有名字传入，则直接返回
        if name is None:
            print(f'INFO: there is no input name')
            return

        profile = Profile.objects.filter(name=name).first()
        if profile:  # 如果存在匹配的Profile对象，则将其分配给Face模型的外键字段
            old_name = fc_instance.profile.name if fc_instance.profile else 'unknown'
            new_name = name
            print(f'人脸更新：新的人脸是 {old_name} --> {new_name}')
            if not profile.embedding:
                print(f'INFO: this profile has no embedding, update embedding')
                profile.embedding = fc_instance.embedding
                profile.save()

            if old_name != new_name:
                # 如果存在匹配的Profile对象，则将其分配给Face模型的外键字段
                print(f'INFO: this name of profile already existed: {new_name}')
                print(f'INFO: fc_instance.profile before is {fc_instance.profile.id}')
                fc_instance.profile = profile
                fc_instance.save()
                print(f'INFO: fc_instance.profile after is {fc_instance.profile.id}')

        else:  # 如果不存在匹配的Profile对象，则创建一个新的Profile对象
            try:
                # 创建一个新用户profile对象，设定默认密码为666，加密保存，User中is_active设置为0， username设置成name，
                # 如果username已经存在相同字段，则在name后面增加4位随机数，再次创建保存
                username = name
                while Profile.objects.filter(username=username).exists():
                    # 生成4位随机数，并与name拼接
                    random_suffix = str(random.randint(1000, 9999))
                    username = f'{name}{random_suffix}'

                full_pinyin, lazy_pinyin = get_pinyin(name)
                # creation_params = {
                #     'username': username,
                #     'password': make_password('deep-diary666'),
                #     'name': name,
                #     'full_pinyin': full_pinyin,
                #     'lazy_pinyin': lazy_pinyin,
                #     'avatar': fc_instance.src,  # 需要对avatar进行赋值
                #     'embedding': fc_instance.embedding,
                # }
                # profile, created = Profile.objects.get_or_create(name=username, defaults=creation_params)

                profile = Profile.objects.create_user(username=username,
                                                      password=make_password('deep-diary666'),
                                                      is_active=0,
                                                      name=name,
                                                      full_pinyin=full_pinyin,
                                                      lazy_pinyin=lazy_pinyin,
                                                      embedding=fc_instance.embedding,
                                                      avatar=fc_instance.src)

                fc_instance.profile = profile
                fc_instance.face_score = 1  # 人脸识别分数, 重命名后，说明经过人工确认，就是属于这个人的，因此概率为100%
                fc_instance.save()
                print(f'INFO: success created a new profile: {profile.name}')

            except IntegrityError:
                print('ERROR: Failed to create a new profile. IntegrityError occurred.')
            # 更新人物资产
            # 如果profile 存在，则将外键asserts中的face_cnt+1
            # 查找或创建asserts对象
            # process = ProfileProcess()
            # process.get_asserts(instance=profile)
            ProfileProcess.get_asserts(instance=profile)

            # asserts, created = Assert.objects.get_or_create(profile=profile)
            # # 将外键asserts中的face_cnt+
            # # asserts.face_cnt = F('face_cnt')+1
            # # asserts.img_cnt = F('img_cnt')+1
            # asserts.face_cnt = profile.faces.count()
            # asserts.img_cnt = profile.imgs.count()
            # asserts.save()

        return profile, fc_instance

    def add_parent_category(self, instance=None):
        """
        :param instance: the instance of the image
        :return:
        """
        pass


@shared_task
def check_img_info(instance, get_list=None, add_list=None, force=False):
    print('check_img_info ...')
    # if get_list is None:
    #     get_list = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories',
    #                 'get_faces']
    # if add_list is None:
    #     add_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
    #                 'add_colors_to_category']
    # print(f'INFO:-> param force: {force}')
    # print(f'INFO:-> param get_list: {get_list}')
    # print(f'INFO:-> param add_list: {add_list}')

    img_process = ImgProces()
    img_process.get_img(img_process, instance=instance, func_list=get_list, force=force)
    img_process.add_img_to_category(img_process, instance=instance, func_list=add_list)


@shared_task
def check_all_img_info(get_list=None, add_list=None, force=False):
    # print('check_all_img_info ...')
    # if get_list is None:
    #     get_list = ['get_exif_info', 'get_tags', 'get_colors', 'get_categories',
    #                 'get_faces']
    # if add_list is None:
    #     add_list = ['add_date_to_category', 'add_location_to_category', 'add_group_to_category',
    #                 'add_colors_to_category']
    # print(f'INFO:-> param force: {force}')
    # print(f'INFO:-> param get_list: {get_list}')
    # print(f'INFO:-> param add_list: {add_list}')

    img_process = ImgProces()
    img_process.get_all_img(img_process, func_list=get_list, force=force)

    img_process.add_all_img_to_category(img_process, func_list=add_list)


@shared_task
def test(value):
    print(f'INFO: periodic task: the value is {value}')
    return f'success received the value: {value}'
