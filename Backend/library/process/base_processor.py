import base64
import logging
import os
import uuid
from io import BytesIO

import cv2
import numpy as np
import pyexiv2
import requests
from PIL import Image
# from django.core.files import File
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from library.models import Img
from utilities.common import trace_function, generate_unique_name, end_color, highlight_color

logger = logging.getLogger(__name__)


class ImageProcessor:
    def __init__(self, img=None):
        if not img:
            print(f'{highlight_color}ERROR: No image provided.{end_color}')
            logger.error(f'{highlight_color}ERROR: No image provided.{end_color}')
        self.img = img  # 图片对象
        self.img_type, self.path = self.get_img_type()  # 图片类型
        print(f'{highlight_color}get the img:{self.img}, {self.img_type},{self.path}.{end_color}')
        logger.error(f'{highlight_color}get the img:{self.img}, {self.img_type},{self.path}.{end_color}')

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
    def get_img_type(self):
        """
        获取输入对象类型。
        """
        img = self.img

        if isinstance(img, Img) and img.src and not img.src.name == 'sys_img/logo_lg.png':
            obj_type = 'instance'
            path = img.src.url  # 使用oss path
        elif isinstance(img, TemporaryUploadedFile):
            obj_type = 'TemporaryUploadedFile'
            path = img.get_temporary_file_path()
        elif isinstance(img, InMemoryUploadedFile):
            obj_type = 'InMemoryUploadedFile'
            path = None
        elif isinstance(img, str) and os.path.isfile(img):
            obj_type = 'path'
            path = img
        elif isinstance(img, str) and img.startswith(('http://', 'https://')):
            obj_type = 'url'
            path = img
        elif isinstance(img, (bytes, bytearray)):
            obj_type = 'bytes'
            path = None
        else:
            print(f'{highlight_color}ERROR: Unsupported image type, {type(img)},{img}.{end_color}')
            logger.error(f'{highlight_color}ERROR: Unsupported image type, {type(img)},{img}.{end_color}')
            obj_type = None
            path = None
        return obj_type, path

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
    def face_crop(image, bbox, name):
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
        # 构造人脸图片名字
        face_name = generate_unique_name() + '.jpg'  # 随机生成5位字符串作为人脸名字
        # 创建并返回一个 Django File 对象
        file = File(image_stream, name=face_name)

        return file
