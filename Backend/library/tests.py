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
# from library.imagga import imagga_post
# from library.serializers import ColorSerializer, ColorBackgroundSerializer, ColorForegroundSerializer, ColorImgSerializer
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
# django.setup()
# from library.models import Img, ColorBackground, ColorForeground, ColorImg, Color, Category, ImgCategory
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
# def set_img_categories(img_obj):
#     img_path = img_obj.src.path
#     endpoint = 'categories/personal_photos'
#
#     response = imagga_post(img_path, endpoint)
#     # with open("categories.txt", 'wb') as f:  # store the result object, which will helpful for debugging
#     #     pickle.dump(response, f)
#
#     # with open("categories.txt",
#     #           'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
#     #     response = pickle.load(f)
#
#     if 'result' in response:
#         categories = response['result']['categories']
#         categories_list = []
#         img_cate_list = []
#         data = {}
# 
#         for item in categories:
#             # obj = Category(name=item['name']['en'], confidence=item['confidence'])
#             checkd_obj = Category.objects.filter(name=item['name']['en'])
#             if checkd_obj.exists():
#                 # print(f'--------------------categories have already existed---------------------------')
#                 # return
#                 obj = checkd_obj.first()
#             else:
#                 obj = Category.objects.create(name=item['name']['en'])
#
#             if ImgCategory.objects.filter(img=img_obj, category=obj).exists():
#                 print(f'--------------------ImgCategory have already existed---------------------------')
#                 continue
#             item = ImgCategory(img=img_obj, category=obj, confidence=item['confidence'])
#             img_cate_list.append(item)
#             categories_list.append(obj)
#
#         print(img_cate_list)
#         ImgCategory.objects.bulk_create(img_cate_list)
#
#         # img_obj.categories.add(*categories_list, through_defaults=confidence_list)
#
#         print(
#             f'--------------------{img_obj.id} :categories have been store to the database---------------------------')
#
# img_obj = Img.objects.get(pk=426)
# set_img_categories(img_obj)
#
#
# print('--------------------end---------------------------')
