import io
import mimetypes
from django.test import TestCase
import django

# Create your tests here.
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_oss_storage.backends import OssStorage
from django_redis import get_redis_connection

from deep_diary import settings
from deep_diary.config import api_key, api_secret
from library.serializers import ImgSerializer



class MyModelTestCase(TestCase):
    def setUp(self):
        # 设置测试环境
        # 创建测试数据
        pass

    def test_something(self):
        # 编写测试代码
        pass

    def test_another_thing(self):
        # 编写测试代码
        pass




# fpath = r'd:\test images\IMG_20210909_194805.jpg'
# with open(fpath,
#           'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited

fpath = r'https://deep-diary.oss-accelerate.aliyuncs.com/media/blue/img/IMG_20210909_194805_acSEpvt.jpg'
fname = 'demo.jpg'






print('--------------------end---------------------------')
print(f'\033[1;32m --------INFO:img address have been created to the database-------- \033[0m')
