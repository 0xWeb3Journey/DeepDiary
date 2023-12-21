import base64
import bisect
import json
import os
import random
import string
from datetime import datetime
from functools import wraps
from io import BytesIO
from tempfile import NamedTemporaryFile

import clip
import cv2
import numpy as np
import pyexiv2
import requests
import torch
from PIL import Image
from celery import shared_task
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# from django.core.files import File
from django.core.files.base import File
from django.core.files.storage import default_storage

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db import transaction, IntegrityError
from django.db.models import F
from insightface.app import FaceAnalysis
from lavis.models import load_model_and_preprocess
from sklearn.metrics.pairwise import cosine_similarity
from taggit.models import Tag

from deep_diary.settings import cfg, calib
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.imagga import imagga_get
from library.models import Img, Category, Face, \
    FaceLandmarks3D, FaceLandmarks2D, Kps, Stat, Address, Evaluate, Date
from library.serializers import McsDetailSerializer, ColorSerializer, ColorBackgroundSerializer, \
    ColorForegroundSerializer, ColorImgSerializer, FaceSerializer
from user_info.models import Profile, Assert
from user_info.task import ProfileProcess
# from utils.mcs_storage import upload_file_pay

from pypinyin import lazy_pinyin, pinyin, Style
from django.db import transaction
from typing import Any, Dict, Type

from utilities.common import trace_function, get_pinyin
from utilities.mcs_storage import upload_file_pay

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


# def get_pinyin(name):
#     if name is None:
#         return None, None
#     # full_pinyin = ''.join([item[0] for item in pinyin(name, style=Style.NORMAL)])
#     full_pinyin = ''.join(lazy_pinyin(name))
#     lazy_pinyin_str = ''.join(lazy_pinyin(name, style=Style.FIRST_LETTER))
#     return full_pinyin, lazy_pinyin_str


class ImageProcessor:
    def __init__(self, img=None):
        self.img = img  # 图片对象

        # 初始化图像数据
        self.img_exiv2 = None
        self.img_pil = None
        self.img_cv2 = None
        self.base64 = None
        self.img_bytes = None
        self.exif = None
        self.xmp = None
        self.iptc = None

        # 读取并存储图像数据
        # self.read(img)

    def load_image_data(self, img_content):
        """
        加载图像内容并转换为不同格式。
        """
        self.img_bytes = img_content
        self.base64 = base64.b64encode(img_content)
        try:
            self.img_exiv2 = pyexiv2.ImageData(img_content)
        except RuntimeError as e:
            print(f"Unable to load image data with pyexiv2: {e}")
            self.img_exiv2 = None
        self.img_pil = Image.open(BytesIO(img_content))
        img_np_array = np.frombuffer(img_content, np.uint8)
        self.img_cv2 = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

        return self.img_exiv2, self.img_pil, self.img_cv2

    @trace_function
    def read(self):
        """
        读取并处理图像。
        """
        # 重置所有图像数据
        img = self.img

        if isinstance(img, Img) and img.src and not img.src.name == 'sys_img/logo_lg.png':
            img_content = default_storage.open(img.src.name).read() if default_storage.exists(
                img.src.name) else requests.get(img.src.url).content
        elif isinstance(img, TemporaryUploadedFile):
            with open(img.temporary_file_path(), 'rb') as f:
                img_content = f.read()
        elif isinstance(img, InMemoryUploadedFile):
            img.seek(0)
            img_content = img.read()
            img.seek(0)  # 重置文件指针
        elif isinstance(img, str) and os.path.isfile(img):
            with open(img, 'rb') as f:
                img_content = f.read()
        elif isinstance(img, str) and img.startswith(('http://', 'https://')):
            img_content = requests.get(img).content
        elif isinstance(img, (bytes, bytearray)):
            img_content = img
        else:
            print('ERROR: Unsupported image type')
            return None

        # 读取并转换图像内容
        self.load_image_data(img_content)
        self.read_img_info()

        return self.img_exiv2, self.img_pil, self.img_cv2

    def read_img_info(self):
        """
        读取EXIF数据。
        """
        try:
            self.exif = self.img_exiv2.read_exif() if self.img_exiv2 else None
            self.xmp = self.img_exiv2.read_xmp() if self.img_exiv2 else None
            self.iptc = self.img_exiv2.read_iptc() if self.img_exiv2 else None
        except (AttributeError, UnicodeDecodeError) as e:
            print(f'INFO: get_date----->UnicodeDecodeError {e} ')

    def get(self, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method.")

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
        # file_stream = BytesIO()
        # face_image.save(file_stream, format='JPEG')
        # file_stream.seek(0)
        # # 构造人脸图片名字
        # face_name = ''.join(random.sample(string.ascii_letters + string.digits, 5)) + '.jpg'  # 随机生成5位字符串作为人脸名字
        # # 将文件流的内容读取为字节数据
        # file_data = file_stream.getvalue()
        # # 构造文件对象
        # file = InMemoryUploadedFile(file_stream, None, face_name, 'image/jpeg', len(file_data), None)

        # 构造 TemporaryUploadedFile 对象
        # temp_file = NamedTemporaryFile(delete=False, suffix='.jpg')
        # face_image.save(temp_file, format='JPEG')
        # temp_file.close()
        # # 读取临时文件并创建TemporaryUploadedFile对象
        # temp_file = open(temp_file.name, 'rb')
        # file = TemporaryUploadedFile(
        #     name=temp_file.name,
        #     content_type='image/jpeg',
        #     size=os.path.getsize(temp_file.name),
        #     charset=None
        # )

        # 构造 django.core.files.base import File 对象
        # 将裁剪得到的图像保存到 BytesIO 流
        image_stream = BytesIO()
        face_image.save(image_stream, format='JPEG')
        image_stream.seek(0)

        # 创建并返回一个 Django File 对象
        file = File(image_stream, name='temp_face.jpg')

        return file


class ExifProcessor(ImageProcessor):
    # ... 其他方法 ...

    def get(self, *args, **kwargs):
        if not self.exif:
            return None
        exif = {
            'date': self.get_date(),
            'addr': self.get_addr(),
            'eval': self.get_eval(),
            'base': self.get_base(),
            'tags': self.get_tags(),
        }
        print(f'exif is {exif}')
        return exif

    @staticmethod
    def resolve_date(date_str):
        # 解析日期的静态方法
        if not date_str:
            date_str = '1970:01:01 00:00:00'
        tt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        date = {
            'capture_date': tt.strftime("%Y-%m-%d"),
            'capture_time': tt.strftime("%H:%M:%S"),
            'year': str(tt.year).rjust(2, '0'),
            'month': str(tt.month).rjust(2, '0'),
            'day': str(tt.day).rjust(2, '0'),
            'is_weekend': tt.weekday() >= 5,
            'earthly_branches': bisect.bisect_right(calib['hour_slot'], tt.hour) - 1,
        }
        return date

    @trace_function
    def get_date(self):

        # deal with timing
        date_str = self.exif.get('Exif.Photo.DateTimeOriginal',
                                 '1970:01:01 00:00:00') if self.exif else '1970:01:01 00:00:00'

        date_dict = self.resolve_date(date_str)  # return the date instance
        return date_dict

    @trace_function
    def get_addr(self):

        exif = self.exif

        print(f'INFO: get_addr----->exif is true ')

        longitude = GPS_format(exif.get('Exif.GPSInfo.GPSLongitude', None))
        latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude', None))
        altitude = exif.get('Exif.GPSInfo.GPSAltitude', None)  # 根据高度信息，最终解析成float 格式
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

        return addr

    @trace_function
    def get_eval(self):
        rate = {
            'rating': int(self.xmp.get('Xmp.xmp.Rating', 0)),
        }
        return rate

    @trace_function
    def get_base(self):

        exif = self.exif
        iptc = self.iptc
        xmp = self.xmp
        img_pil = self.img_pil

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
        return base

    @trace_function
    def get_tags(self):
        return self.iptc.get('Iptc.Application2.Keywords', []) if self.iptc else []


# class FaceProcessor(ImageProcessor):
#     # ... 其他方法 ...
#     # def __init__(self, image_processor):
#
#     def __init__(self, img=None):
#         super().__init__(img)
#         self.app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
#         self.app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=calib['face']['det_threshold'])  # 默认det_thresh=0.5,
#         self.enableLM = True
#         self.is_need_recognize = True
#
#     @trace_function
#     def get(self, *args, **kwargs):
#         faces = []
#         LMnames = []
#         LMbboxs = []
#         ins_fcs = self.app.get(self.img_cv2)
#         if self.enableLM and self.xmp:  # 通过LM方式检测到了人脸
#             LMnames, LMbboxs = self.get_lm_face_info()
#         for face in ins_fcs:
#             pose = face.pose.astype(np.float16)
#             bbox = np.round(face.bbox).astype(np.int16)
#             name, face_score = self.get_name(LMnames, LMbboxs, face.bbox)
#             if face_score == 1:  # 通过LM方式检测到了人脸
#                 self.is_need_recognize = False
#
#             fc = {
#                 'img': None,  # 后续在处理数据库保存的时候再对其赋值
#                 'profile': name,  # 后续在处理数据库保存的时候再对其赋值
#                 'det_score': face.det_score,
#                 'face_score': face_score,
#                 'is_confirmed': True if face_score == 1 else False,
#                 # 如果是self.is_need_recognize = True,则需要进行人脸识别，然后对其再次赋值
#                 'src': self.face_crop(self.img_pil, bbox),  # 需要对src进行赋值
#                 'age': face.age,
#                 'gender': face.gender,
#                 'embedding': face.normed_embedding.astype(np.float16).tobytes(),
#                 'pose_x': pose[0],
#                 'pose_y': pose[1],
#                 'pose_z': pose[2],
#                 'x': bbox[0],
#                 'y': bbox[1],
#                 'wid': bbox[2] - bbox[0],
#                 'height': bbox[3] - bbox[1],
#             }
#             data = {
#                 'fc': fc,
#                 'kps': np.round(face.kps).astype(np.int16),
#                 'landmarks2d': np.round(face.landmark_2d_106).astype(np.int16),
#                 'landmarks3d': np.round(face.landmark_3d_68).astype(np.int16),
#                 'profile': name,
#             }
#             faces.append(data)
#
#         return faces
#
#     def get_lm_face_info(self):
#         print(f'INFO: get_LM_face_info STARTED ... ')
#         num = 1  # xmp 内容下表从1开始
#         is_have_face = True
#         names = []
#         bboxs = []
#         xmp = self.xmp
#         # print(f'INFO: xmp is {json.dumps(xmp, indent=4)}')
#         while is_have_face:
#             item = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Type'.format(num)
#             is_have_face = xmp.get(item, None)
#             if is_have_face:
#                 # print(f'INFO: LM face detected')
#                 idx_name = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Name'.format(num)
#                 idx_h = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:h'.format(num)
#                 idx_w = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:w'.format(num)
#                 idx_x = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:x'.format(num)
#                 idx_y = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Area/stArea:y'.format(num)
#                 num += 1
#
#                 name = xmp.get(idx_name, 'unknown')
#                 names.append(name)
#                 lm_face_area = [xmp.get(idx_x), xmp.get(idx_y), xmp.get(idx_w), xmp.get(idx_h)]  # 0~1 之间的字符
#                 lm_face_area = np.array(lm_face_area).astype(float)  # 0~1 之间的浮点，中心区域，人脸长，宽
#                 bbox = self.face_zoom(lm_face_area, 1, self.img_pil.width,
#                                       self.img_pil.height)  # 转变成像素值，左上区域和右下区域坐标，跟insightface 保持一致
#                 bboxs.append(bbox)
#         # print(f'INFO: the LM names is {names}, bbox is {bboxs}')
#         print(f'INFO: get_LM_face_info END ... ')
#
#         return names, bboxs
#
#     @staticmethod
#     def face_zoom(area, ratio, width, height):  # area: 中心坐标，宽度，高度
#         [x, y, w, h] = area
#
#         w = w * ratio
#         h = h * ratio
#         x1 = max(x - w / 2, 0)
#         y1 = max(y - h / 2, 0)
#         x2 = min(x1 + w, 1)
#         y2 = min(y1 + h, 1)
#         # print(f'INFO: the face width is {width}, face height is {height}')
#         bbox = [x1 * width, y1 * height, x2 * width, y2 * height]
#
#         return np.array(bbox).astype(int)
#
#     def get_name(self, names, LMbboxs, bbox):
#         print(f'INFO: get_name STARTED ... ')
#         name = 'unknown'
#         score = 0
#         if len(names) > 0:
#             for i in range(len(names)):
#                 if self.compute_iou(LMbboxs[i], bbox):
#                     name = names[i]
#                     score = 1
#                     break
#         print(f'INFO: get_name END ... ')
#         return name, score
#
#     @staticmethod
#     def compute_iou(rec1, rec2):  # 这里的矩形，包括左上角坐标和右下角坐标
#         """
#         计算两个矩形框的交并比。
#         :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
#         :param rec2: (x0,y0,x1,y1)
#         :return: 交并比IOU.
#         """
#         iou = 0
#         rst = False
#         left_column_max = max(rec1[0], rec2[0])
#         right_column_min = min(rec1[2], rec2[2])
#         up_row_max = max(rec1[1], rec2[1])
#         down_row_min = min(rec1[3], rec2[3])
#         # 两矩形无相交区域的情况
#         if left_column_max >= right_column_min or down_row_min <= up_row_max:
#             rst = False
#         # 两矩形有相交区域的情况
#         else:
#             S1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
#             S2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])
#             S_cross = (down_row_min - up_row_max) * (right_column_min - left_column_max)
#             iou = S_cross / (S1 + S2 - S_cross)
#             if iou > 0.5:
#                 rst = True
#
#         print(f'INFO: computed_iou is {iou} ... ')
#
#         return rst


class TagProcessor(ImageProcessor):
    """
    图像标签处理。
    """

    def __init__(self, image_processor):
        self.image_processor = image_processor

    def get(self, *args, **kwargs):
        return None


class ColorProcessor(ImageProcessor):
    """
    图像颜色处理。
    """

    def __init__(self, image_processor):
        self.image_processor = image_processor

    def get(self, *args, **kwargs):
        return None


class CategoryProcessor(ImageProcessor):
    """
    图像分类处理。
    """

    def __init__(self, image_processor):
        self.image_processor = image_processor

    def get(self, *args, **kwargs):
        return None


class FeatureProcessor(ImageProcessor):
    """
    图像特征提取处理。
    """

    def __init__(self, image_processor):
        self.image_processor = image_processor

    def get(self, *args, **kwargs):
        return None


class CaptionProcessor(ImageProcessor):
    """
    图像描述生成处理。
    """

    def __init__(self, image_processor):
        self.image_processor = image_processor

    def get(self, *args, **kwargs):
        return


# class ProcessorManager:
#     def __init__(self, img):
#         self.img_processor = ImageProcessor(img)
#         self.img_processor.read()
#         self.processors = {
#             'exif': ExifProcessor,
#             'face': FaceProcessor,
#             'tag': TagProcessor,
#             'color': ColorProcessor,
#             'category': CategoryProcessor,
#             'feature': FeatureProcessor,
#             'caption': CaptionProcessor,
#             # ... 其他类型 ...
#         }
#
#     def get(self, processor_type, attributes=None, *args, **kwargs):
#         # 获取带有所需数据的处理器并调用其get方法
#         processor = self.get_processor(processor_type, attributes)
#         return processor.get(*args, **kwargs)
#
#     def get_processor(self, processor_type, attributes=None):
#         # 根据类型初始化对应的处理器
#
#         processor_cls = self.processors.get(processor_type)
#         if not processor_cls:
#             raise ValueError(f"Processor type '{processor_type}' is not supported.")
#
#         processor = processor_cls()
#         if attributes is None:
#             attributes = [attr for attr in dir(self.img_processor) if
#                           not attr.startswith("__") and not callable(getattr(self.img_processor, attr))]
#         print(f'INFO: get_processor----->attributes is {attributes} ')
#
#         # 根据属性列表选择性地传递图像数据给处理器
#         for attribute in attributes:
#             if hasattr(self.img_processor, attribute):
#                 setattr(processor, attribute, getattr(self.img_processor, attribute))
#
#         return processor


class SaveStrategy:
    def __init__(self, instance):
        self.instance = instance
        self.stats, _ = Stat.objects.get_or_create(img=self.instance)

    @staticmethod
    def check_data_validity(data) -> bool:
        """
        检查数据是否有效, 如果全为空，则返回False。否则返回True。
        """
        # 判断data数据类型，如果是dict
        if isinstance(data, dict):
            # 如果字典中至少有一个值不是None，则返回True
            return any(value is not None for value in data.values())
        # 如果是list
        elif isinstance(data, list):
            # 如果列表不为空，则返回True，否则返回False
            return bool(data)
        else:
            # 非字典和非列表类型，无法判断有效性，返回False
            return False

    def update_stats_flag(self, flag_field: str) -> None:
        """
        更新图片实例stats的对应标志位。
        """
        setattr(self.stats, flag_field, True)
        self.stats.save()

    def save(self, data) -> None:
        raise NotImplementedError


class ExifSaveStrategy(SaveStrategy):
    @transaction.atomic
    @trace_function
    def save(self, data) -> None:
        # 具体的EXIF保存逻辑
        if not self.check_data_validity(data):
            print(f"No EXIF data to process for img {self.instance.id}.")
            return

        # TODO 如果已经存在exif数据，则清除所有外键关联数据
        # 清除实例的所有标签
        self.instance.tags.clear()

        # 标志位字段名称，可以根据实际情况调整

        field = 'is_get_info'
        data_to_save = {
            Address: data.get('addr', None),
            Evaluate: data.get('eval', None),
            Date: data.get('date', None),
        }
        self.save_data(data_to_save, field)
        self._save_base_and_tags(data.get('base', None), data.get('tags', []))

    def save_data(self, data, field):
        """
        通用保存数据方法。
        """
        # 检查所有字段是否为空，如果是，则设置 no_exif 标志
        if not self.check_data_validity(data):
            setattr(self.stats, 'is_has_exif', False)
            self.stats.save()
            print(f"No EXIF data to process for img {self.instance.id}.")
            return

        with transaction.atomic():
            for model, data_dict in data.items():
                if data_dict is not None:
                    self._update_or_create_data(model, data_dict, field)
            self.update_stats_flag(field)
            print(f"EXIF data saved for img {self.instance.id}.")

    def _save_base_and_tags(self, base_data, tags):
        """
        保存基础信息和标签。
        """
        self.instance.__dict__.update(base_data)
        self.instance.save()
        if tags:
            print(f"INFO: the tags is {tags} ")
            self.instance.tags.add(*tags)

    def _update_or_create_data(self, model, data_dict, field_name):
        """
        更新或创建数据。
        """

        obj, created = model.objects.update_or_create(
            img=self.instance, defaults=data_dict
        )
        return obj


class FaceSaveStrategy(SaveStrategy):

    @trace_function
    @transaction.atomic
    def save(self, data) -> None:
        """
        将人脸检测数据保存到数据库。
        """
        # 保存逻辑...
        if not self.check_data_validity(data):
            print(f"No face data to process for img {self.instance.id}.")
            return

        field = 'is_get_face'

        # 如果已经存在人脸数据，则清除所有人脸数据
        Face.objects.filter(img=self.instance).delete()
        self.instance.profiles.clear()

        kps_to_create = []
        landmarks3d_to_create = []
        landmarks2d_to_create = []

        for fc_data in data:  # data 是个人脸列表
            profile, created = self.get_profile(fc_data)
            fc = fc_data['fc']
            fc['img'] = self.instance
            fc['profile'] = profile

            # 创建Face对象
            face = Face.objects.create(**fc)
            # face = Face.objects.create(img=fc['img'], profile=fc['profile'], det_score=fc['det_score'], src=fc['src'])
            print(f'INFO: the face is {face.id} ')
            # 更新人物资产，比如新增了一张人脸，那么人物资产中的人脸数目就要加1
            ProfileProcess.get_asserts(instance=profile)

            for kps_data in fc_data['kps']:
                # kps_obj = Kps(face=face, *kps_data)
                kps_obj = Kps(face=face, x=kps_data[0], y=kps_data[1])
                kps_to_create.append(kps_obj)

            for landmark_data in fc_data['landmarks3d']:
                # lm3d_obj = FaceLandmarks3D(face=face, *landmark_data)
                lm3d_obj = FaceLandmarks3D(face=face, x=landmark_data[0], y=landmark_data[1], z=landmark_data[2])
                landmarks3d_to_create.append(lm3d_obj)

            for landmark_data in fc_data['landmarks2d']:
                # lm2d_obj = FaceLandmarks2D(face=face, *landmark_data)
                lm2d_obj = FaceLandmarks2D(face=face, x=landmark_data[0], y=landmark_data[1])
                landmarks2d_to_create.append(lm2d_obj)

        # 批量创建其他相关对象
        Kps.objects.bulk_create(kps_to_create)
        FaceLandmarks3D.objects.bulk_create(landmarks3d_to_create)
        FaceLandmarks2D.objects.bulk_create(landmarks2d_to_create)

        self.update_stats_flag(field)
        print(f"Face data saved for img {self.instance.id}.")

    @trace_function
    def get_profile(self, fc):
        face = fc['fc']
        face_name = fc['profile']
        #  尝试获取face_name对应的profile，如果不存在，则创建一个新的profile
        try:
            profile = Profile.objects.get(name=face_name)
            print(f'INFO: the profile already existed: {profile.name}')
            return profile, False
        except Profile.DoesNotExist:
            # 处理不存在结果的情况
            username = face_name
            try:
                # 创建一个新用户profile对象，设定默认密码为666，加密保存，User中is_active设置为0， username设置成name，
                # 如果username已经存在相同字段，则在name后面增加4位随机数，再次创建保存
                while Profile.objects.filter(username=username).exists():
                    # 生成4位随机数，并与name拼接
                    random_suffix = str(random.randint(1000, 9999))
                    username = f'{face_name}{random_suffix}'
                print(f'INFO: will create a new profile, the username is : {username}, name is {face_name}')
            except IntegrityError:
                print('ERROR: Failed to create a new profile. IntegrityError occurred.')

            full_pinyin, lazy_pinyin = get_pinyin(face_name)
            creation_params = {
                'username': username,
                'password': make_password('deep-diary666'),
                'name': face_name,
                'full_pinyin': full_pinyin,
                'lazy_pinyin': lazy_pinyin,
                'avatar': face['src'],
                'embedding': face['embedding'],
            }
            # 根据creation_params创建一个新的profile
            profile = Profile.objects.create(**creation_params)
            print(f'INFO: success created a new profile: {profile.name}')
            return profile, True
        except Profile.MultipleObjectsReturned:
            # 处理多个结果的情况
            pass


class DatabaseSaver:
    """
    负责将数据保存到数据库的类。
    """

    def __init__(self, instance):

        if not isinstance(instance, Img):
            raise ValueError("Instance must be an Img instance")
        self.instance = instance
        self.strategy = None
        self.strategies = {
            'exif': ExifSaveStrategy,
            'face': FaceSaveStrategy,
            # ... 其他类型 ...
        }

    def set_strategy(self, strategy_type: str) -> SaveStrategy:
        strategy_cls = self.strategies.get(strategy_type)
        if not strategy_cls:
            raise ValueError(f"Strategy type '{strategy_type}' is not supported.")
        self.strategy = strategy_cls(self.instance)
        return self.strategy

    @trace_function
    def save(self, data) -> None:
        self.strategy.save(self.instance, data)


# class ProcessingController:
#     def __init__(self, img=None, instance=None):
#         self.manager = ProcessorManager(img)
#         self.instance = self.get_image_instance(instance)
#         self.db_saver = DatabaseSaver(self.instance)
#         self.stats, _ = Stat.objects.get_or_create(img=self.instance)
#         self.fields = {
#             'exif': 'is_get_exif',
#             'face': 'is_get_face',
#             'tag': 'is_get_tag',
#             'color': 'is_get_color',
#             'category': 'is_get_category',
#             'feature': 'is_get_feature',
#             'caption': 'is_get_caption',
#             # ... 其他类型 ...
#         }
#
#     def get_image_instance(self, img):
#         # 如果instance是Img实例，则直接返回
#         instance = None
#         if isinstance(img, Img):
#             instance = img
#         # 如果instance是本地路径，则首先获取其文件名，然后根据文件名获取Img实例
#         elif isinstance(img, str) and os.path.exists(img) and os.path.isfile(img):
#             filename = os.path.basename(img)
#             try:
#                 instance = Img.objects.get(name=filename)
#             except Img.DoesNotExist:
#                 print(f"Img instance with name '{filename}' does not exist.")
#
#         return instance
#
#     def _is_need_process(self, field, force=False):
#         """
#         检查是否需要处理数据库保存操作。
#         """
#         if not field:
#             return False
#         value = getattr(self.stats, field, False)
#         if force or not value:
#             setattr(self.stats, field, True)
#             self.stats.save()
#             return True
#         print(f"{field} already processed for img {self.instance.id}. Set force=True to override.")
#         return False
#
#     @trace_function
#     def process_and_save(self, processor, force=False, *args, **kwargs):
#         """
#         处理图像数据并将结果保存到数据库。
#         """
#
#         #  检查是否有必要执行处理操作
#         print(f'INFO: process_and_save----->processor is {processor} ')
#         if not self._is_need_process(self.fields.get(processor, None), force):
#             print(f"No need to process {processor} for img {self.instance.id}.")
#             return
#
#         data = self.manager.get(processor, *args, **kwargs)
#         save_method = self.db_saver.set_strategy(processor)
#         if save_method is None:
#             raise ValueError(f"No save method for processor type '{processor}'")
#         save_method.save(data)


# 使用示例
# img_instance = Img.objects.all().first()
# path = r'd:\BlueDoc\DiaryWin\source\img\已上传\IMG_20200815_151915.jpg'
# controller = ProcessingController(path, img_instance)
# controller.process_and_save('exif', force=True)
# controller.process_and_save('exif', force=False)


@shared_task
@trace_function
def save_img(img_id, f_path=None, processor_type=None, force=False):
    # This is the asynchronous task that saves the image and returns the instance. If the serializer and user
    # need to be passed to the Celery task, you will need to make sure they are serializable or pass their IDs
    # instead.
    print(f'INFO: save_img STARTED ... ')


@shared_task
@trace_function
def post_process(img_id, f_path=None, processor_types=None, force=False, index=1, total_imgs=1):
    if processor_types is None:
        processor_types = ['exif']
    # img_ins = Img.objects.get(pk=img_id)
    # img = f_path if f_path else img_ins
    # controller = ProcessingController(img=img, instance=img_ins)
    # for processor_type in processor_types:
    #     print(f'INFO: Processing image {index}/{total_imgs} (ID: {img.id}, processor_type: {processor_type}).')
    #     controller.process_and_save(processor_type, force=force)




@shared_task
@trace_function
def process_all(processor_types=None, force=False):
    # Set default processor types if none provided
    if processor_types is None:
        processor_types = ['exif']

    # Filter Img instances based on the processing requirement
    filter_kwargs = {'stats__is_get_{}'.format(pt): True for pt in processor_types}

    imgs = Img.objects.all()
    if not force:
        imgs = imgs.exclude(**filter_kwargs)

    total_imgs = imgs.count()
    print(f'INFO: Total {total_imgs} images to process.')

    for index, img in enumerate(imgs, start=1):
        post_process(img.id, f_path=img, processor_types=processor_types, force=force, index=index,
                     total_imgs=total_imgs)

        completion_percentage = (index / total_imgs) * 100
        print(f'INFO: Image ID {img.id} processing completed. {completion_percentage:.2f}% of total images processed.')

    print('INFO: All images have been processed.')



class ImgProces:
    def __init__(self, img=None):
        """
        path: 图片路径， 可以是本地的，也可以是云存储的, 相对于 media 文件夹的路径
        instance: 图片实体
        procedure: 处理流程，为列表格式['face', 'object', 'caption', 'key point', 'extraction', 'auto tag', 'color', 'classification']
        """

        self.app = None

        self.img = img  # 图片对象, 可以是Img实例，TemporaryUploadedFile实例，InMemoryUploadedFile实例，本地图片，网络图片，二进制文件流

        self.img_exiv2 = None  # pyexiv2.ImageData对象
        self.img_pil = None  # PIL.Image.Image对象
        self.img_cv2 = None  # cv2对象
        self.base64 = None  # 图片二级制文件流
        self.img_bytes = None  # 图片二级制文件流

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.device = torch.device("cpu")

    def load_image_data(self, img_content):
        """
        加载图像内容并转换为不同格式。
        """
        self.img_bytes = img_content
        self.base64 = base64.b64encode(img_content)  # 暂时用不到
        # Attempt to load pyexiv2.ImageData object
        try:
            self.img_exiv2 = pyexiv2.ImageData(img_content)
        except RuntimeError as e:
            print(f"Unable to load image data with pyexiv2: {e}")
            self.img_exiv2 = None
        self.img_pil = Image.open(BytesIO(img_content))
        img_np_array = np.frombuffer(img_content, np.uint8)
        self.img_cv2 = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

        return self.img_exiv2, self.img_pil, self.img_cv2

    def read(self, img):
        # 重置所有图像数据
        self.img_exiv2, self.img_pil, self.img_cv2 = None, None, None

        # 如果img是Img实例或本地文件路径，获取文件内容
        if isinstance(img, Img) and img.src and not img.src.name == 'sys_img/logo_lg.png':
            print('INFO: 有效的Img实例')
            img_content = default_storage.open(img.src.name).read() if default_storage.exists(img.src.name) \
                else requests.get(img.src.url).content
        elif isinstance(img, TemporaryUploadedFile):
            print('INFO: 有效的 TemporaryUploadedFile')
            with open(img.temporary_file_path(), 'rb') as f:
                img_content = f.read()
        elif isinstance(img, InMemoryUploadedFile):
            print('INFO: 有效的 InMemoryUploadedFile')
            img.seek(0)
            img_content = img.read()
            img.seek(0)  # Reset the file pointer after reading
        elif isinstance(img, str) and os.path.isfile(img):
            print('INFO: 有效的本地文件路径 ')
            with open(img, 'rb') as f:
                img_content = f.read()
        elif isinstance(img, str) and img.startswith(('http://', 'https://')):
            print('INFO: 有效的网络图片')
            img_content = requests.get(img).content
        elif isinstance(img, (bytes, bytearray)):
            print('INFO: 有效的二进制文件流')
            img_content = img
        else:
            print('ERROR: Unsupported image type')
            return None

        # 读取并转换图像内容
        self.load_image_data(img_content)

        return self.img_exiv2, self.img_pil, self.img_cv2

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
        print(f"INFO: the fc is {data['fc']} ")
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

    def face_init(self, instance=None):
        if not instance:
            return False
        self.app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.app.prepare(ctx_id=0, det_size=(640, 640), det_thresh=calib['face']['det_threshold'])  # 默认det_thresh=0.5,
        img = self.read_img(instance, ['cv2', 'PIL', 'pyexiv2'])
        self.img_cv2 = img.get('cv2', None)
        self.img_pil = img.get('PIL', None)
        self.img_exiv2 = img.get('pyexiv2', None)

        return True

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
        #  尝试获取face_name对应的profile，如果不存在，则创建一个新的profile
        try:
            profile = Profile.objects.get(name=face_name)
            print(f'INFO: the profile already existed: {profile.name}')
            return profile, False
        except Profile.DoesNotExist:
            # 处理不存在结果的情况
            bbox = np.round(face.bbox).astype(np.int16)
            username = face_name
            try:
                # 创建一个新用户profile对象，设定默认密码为666，加密保存，User中is_active设置为0， username设置成name，
                # 如果username已经存在相同字段，则在name后面增加4位随机数，再次创建保存
                while Profile.objects.filter(username=username).exists():
                    # 生成4位随机数，并与name拼接
                    random_suffix = str(random.randint(1000, 9999))
                    username = f'{face_name}{random_suffix}'
                print(f'INFO: will create a new profile, the username is : {username}, name is {face_name}')
            except IntegrityError:
                print('ERROR: Failed to create a new profile. IntegrityError occurred.')

            full_pinyin, lazy_pinyin = get_pinyin(face_name)
            creation_params = {
                'username': username,
                'password': make_password('deep-diary666'),
                'name': face_name,
                'full_pinyin': full_pinyin,
                'lazy_pinyin': lazy_pinyin,
                'avatar': self.face_crop(self.img_pil, bbox),  # 需要对avatar进行赋值
                'embedding': face.normed_embedding.astype(np.float16).tobytes(),
            }
            # 根据creation_params创建一个新的profile
            profile = Profile.objects.create(**creation_params)
            print(f'INFO: success created a new profile: {profile.name}')
            return profile, True
        except Profile.MultipleObjectsReturned:
            # 处理多个结果的情况
            pass

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

        profile = None
        face_score = 0
        is_need_recognition = True
        # face_name = 'unknown_' + ''.join(random.sample(string.ascii_letters + string.digits, 4))
        # enableLM = False  # 关闭LM方式
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
                print(f"\033[1;32m INFO: LM estimated name is {names[idx]}, iou is {ious[idx]} \033[0m")
                face_name = names[idx]
                face_score = 1
                # 检查Profile 数据库中是否包含此人脸名字
                profile, created = self.create_new_profile(img_ins, face, face_name)
                is_need_recognition = False
            else:  # 最大重合度为0, 可能LM未包含bbox的信息
                print(f"\033[1;32m INFO: can not match the bbox, will start face_recognition \033[0m")
                is_need_recognition = True

        if is_need_recognition:
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
        pass

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
        except (AttributeError, UnicodeDecodeError) as e:
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
        print(f'INFO: get_LM_face_info STARTED ... ')
        num = 1  # xmp 内容下表从1开始
        is_have_face = True
        names = []
        bboxs = []
        # img = self.read_img(instance, ['pyexiv2']).get('pyexiv2', None)
        img = self.img_exiv2
        if img is None:
            print(f'INFO: img is None')
            return names, bboxs
        xmp = img.read_xmp()  # 读取元数据，这会返回一个字典
        # print(f'INFO: xmp is {json.dumps(xmp, indent=4)}')
        while is_have_face:
            item = 'Xmp.mwg-rs.Regions/mwg-rs:RegionList[{:d}]/mwg-rs:Type'.format(num)
            is_have_face = xmp.get(item, None)
            if is_have_face:
                # print(f'INFO: LM face detected')
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
                bbox = self.face_zoom(lm_face_area, 1, instance.wid,
                                      instance.height)  # 转变成像素值，左上区域和右下区域坐标，跟insightface 保持一致
                bboxs.append(bbox)
        # print(f'INFO: the LM names is {names}, bbox is {bboxs}')
        print(f'INFO: get_LM_face_info END ... ')

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
        if stats.is_get_face:
            print(f'INFO: the instance {instance.id} has been processed')
            # 清除Img与Profile之间的多对多关系
            instance.profiles.clear()
            # 清除Img与Profile之间的多对多关系
            instance.faces.all().delete()

        # 2. processing the image
        if not self.face_init(instance=instance):
            return  # 如果没有初始化成功，直接返回
        # image_content = self.read(instance)
        # image_content_obj = BytesIO(image_content)
        # 
        # np_array = np.frombuffer(image_content_obj.getvalue(), np.uint8)
        # image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        # img_pil = Image.open(image_content_obj)

        # img = self.read_img(instance, ['cv2', 'PIL'])
        # img_cv2 = img.get('cv2', None)
        # img_pil = img.get('PIL', None)

        faces = self.app.get(self.img_cv2)
        print(
            f'INFO: get_faces ... the img id is : {instance.id}, total face numbers is {len(faces)}------------------------------')

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
                    'src': self.face_crop(self.img_pil, bbox),  # 需要对src进行赋值
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
        stats.is_get_face = True
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


class ImgOperate:
    def __init__(self, instance=None):
        self.instance = instance

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

    # 现在我需要将各个子模型的分类逻辑，添加到Category中，便于更好的查询，统计，展示
    # 比如Address, Color, Date等模型，将其中的字段按层级提取出来，再保存到Category中，这样就可以通过Category来查询，统计，展示
    # 关于此类的架构，由于涉及到不同模型之间的查询和操作，我的想法是由OperationManager 来管理，
    # 其中一个是get方法，用于从各个模型中提取数据，数据类型为字典类型，然后保存添加到Category中
    # 另一个是add方法，用于将数据添加到Category中
    # 请根据这些描述，基于之前的架构OperationManager管理各个模型的**Operation，**表示模型名称，再帮我增加上述的功能，谢谢
    # 当然，如何有更好的架构和设计，也可以提出来，我们一起讨论
    # 下面是我之前的代码，缺点是1. 不同模型的操作，都再一个函数中； 2 每个方法都有__is_OK_add_to_category__的判断，重复代码太多
    def add_addr_to_category(self, instance=None):
        # 1. get the instance and check if it is OK to add to the category
        instance, process = self.__is_OK_add_to_category__(instance=instance, field='address')
        if not process:
            return
        # 2. get the location
        addr = instance.address
        field_list = [
            'location',
            addr.country if addr.country and addr.country != '[]' else 'No GPS',
            addr.province if addr.province and addr.province != '[]' else 'No GPS',
            addr.city if addr.city and addr.city != '[]' else 'No GPS',
            addr.district if addr.district and addr.district != '[]' else 'No GPS',
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


# @shared_task
# def get_img_info(instance=None, get_list=None, add_list=None, force=False, path=None):
#     print('save_and_get_img_info ...')
#
#     img_process = ImgProces(path=path, instance=instance, url=None)
#     img_process.get_img(img_process, instance=instance, func_list=get_list, force=force)
#     img_process.add_img_to_category(img_process, instance=instance, func_list=add_list)
#
#
# @shared_task
# def check_all_img_info(get_list=None, add_list=None, force=False):
#     # print('check_all_img_info ...'
#
#     img_process = ImgProces()
#     img_process.get_all_img(img_process, func_list=get_list, force=force)
#
#     img_process.add_all_img_to_category(img_process, func_list=add_list)


