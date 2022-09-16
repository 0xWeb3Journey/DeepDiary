# import django
# from django.db.models import Count
# from django.test import TestCase
#
# # Create your tests here.
# import os
#
# from django_redis import get_redis_connection
#
# from deep_diary.config import api_key, api_secret
# from library.serializers import ColorSerializer, ColorBackgroundSerializer, ColorForegroundSerializer, ColorImgSerializer
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
# django.setup()
# from library.models import Img, ColorBackground, ColorForeground, ColorImg, Color
# from face.task import upload_face_to_mcs
# from library.task import upload_img_to_mcs, set_img_tags, set_img_colors
#
# from face.models import FaceAlbum, Face
#
# #
# # # 这里可以传使用哪个redis，不传默认是default
# # redis = get_redis_connection()
# # print(redis)
# # # redis.get(key)
# # # redis.set(key, value)
# import pickle
# import os
# import requests
# from requests.auth import HTTPBasicAuth
#
# ###
# # API Credentials
# API_KEY = api_key  # Set API key here
# API_SECRET = api_secret  # Set API secret here
# ###
#
# ENDPOINT = 'https://api.imagga.com/v2'
#
# FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']
#
#
# class ArgumentException(Exception):
#     pass
#
#
# if API_KEY == 'YOUR_API_KEY' or \
#         API_SECRET == 'YOUR_API_SECRET':
#     raise ArgumentException('You haven\'t set your API credentials. '
#                             'Edit the script and set them.')
#
# auth = HTTPBasicAuth(API_KEY, API_SECRET)
#
#
# image_url = 'https://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'
# img_path = 'https://imagga.com/static/images/nsfw/girl-1211435_960_720.jpg'
#
#
#
# def set_img_colors(img_obj):
#     # this is through post method to get the tags. mainly is used for local img
#     img_path = img_obj.src.path
#     endpoint = 'colors'
#     # color_query = {
#     #     'verbose': False,
#     #     'language': False,
#     #     'threshold': 25.0,
#     # }
#     # response = imagga_post(img_path, endpoint)
#     response = pickle.load(open('response.pkl', 'rb'))
#
#     if response['status']['type'] != 'success':
#         return []
#
#     if 'result' in response:
#         colors = response['result'][endpoint]
#         background_colors = colors['background_colors']
#         foreground_colors = colors['foreground_colors']
#         image_colors = colors['image_colors']
#
#         print(colors)
#
#         # 调用序列化器进行反序列化验证和转换
#         colors.update(img=img_obj.id)
#         serializer = ColorSerializer(data=colors)
#         result = serializer.is_valid(raise_exception=True)
#         color_obj = serializer.save()
#
#         for bk in background_colors:
#             bk.update(color=color_obj.pk)
#             serializer = ColorBackgroundSerializer(data=bk)
#             result = serializer.is_valid(raise_exception=True)
#             back_color_obj = serializer.save()
#
#         for fore in foreground_colors:
#             fore.update(color=color_obj.pk)
#             serializer = ColorForegroundSerializer(data=fore)
#             result = serializer.is_valid(raise_exception=True)
#             fore_color_obj = serializer.save()
#
#         for img in image_colors:
#             img.update(color=color_obj.pk)
#             serializer = ColorImgSerializer(data=img)
#             result = serializer.is_valid(raise_exception=True)
#             img_color_obj = serializer.save()
#
#         print('--------------------all the colors have been store to the database---------------------------')
#
#     #     ColorBackground.objects.bulkcreat()
#     # # back_color_list = [ColorBackground(title=line.split('****')[0], content=line.split('****')[1]) for line in f]
#     #
#     # Blog.objects.bulk_create(BlogList)
#
#
# # img_obj = Img.objects.all().first()
# img_obj = Img.objects.get(pk=432)
# # post_img_tags(img_obj, threshold=30)
# set_img_colors(img_obj)
#
# print('--------------------end---------------------------')
