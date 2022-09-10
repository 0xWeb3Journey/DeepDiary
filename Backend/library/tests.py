import django
from django.db.models import Count
from django.test import TestCase

# Create your tests here.
import os


from django_redis import get_redis_connection
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()
from face.models import FaceAlbum, Face


#
# # 这里可以传使用哪个redis，不传默认是default
# redis = get_redis_connection()
# print(redis)
# # redis.get(key)
# # redis.set(key, value)


fc=Face.objects.all().first()
q = FaceAlbum.objects.filter(id=fc.face_album).annotate(Count('faces'))