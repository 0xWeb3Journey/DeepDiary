import django
from django.db.models import Count
from django.test import TestCase

# Create your tests here.
import os

from django_redis import get_redis_connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()
from library.models import Img
from face.task import upload_face_to_mcs
from library.task import upload_img_to_mcs

from face.models import FaceAlbum, Face


#
# # 这里可以传使用哪个redis，不传默认是default
# redis = get_redis_connection()
# print(redis)
# # redis.get(key)
# # redis.set(key, value)



# upload_to_mcs()