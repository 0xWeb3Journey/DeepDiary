import django
from django.db.models import Count, Q
from django.test import TestCase

# Create your tests here.
import os

from django_redis import get_redis_connection

from deep_diary.config import api_key, api_secret
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.imagga import imagga_post
from library.serializers import ColorSerializer, ColorBackgroundSerializer, ColorForegroundSerializer, \
    ColorImgSerializer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()
from pyexiv2 import Image as exivImg
from library.models import Img, ColorBackground, ColorForeground, ColorImg, Color, Category, ImgCategory, Address, \
    Evaluate, Date
from face.task import upload_face_to_mcs
from library.task import upload_img_to_mcs, set_img_tags, set_img_colors, set_img_date, color_palette

from face.models import FaceAlbum, Face

#
# # 这里可以传使用哪个redis，不传默认是default
# redis = get_redis_connection()
# print(redis)
# # redis.get(key)
# # redis.set(key, value)
import pickle
import os
import requests
from requests.auth import HTTPBasicAuth

###
# API Credentials
API_KEY = api_key  # Set API key here
API_SECRET = api_secret  # Set API secret here
###

ENDPOINT = 'https://api.imagga.com/v2'

FILE_TYPES = ['png', 'jpg', 'jpeg', 'gif']


class ArgumentException(Exception):
    pass


if API_KEY == 'YOUR_API_KEY' or \
        API_SECRET == 'YOUR_API_SECRET':
    raise ArgumentException('You haven\'t set your API credentials. '
                            'Edit the script and set them.')

auth = HTTPBasicAuth(API_KEY, API_SECRET)

image_url = 'https://docs.imagga.com/static/images/docs/sample/japan-605234_1280.jpg'
img_path = 'https://imagga.com/static/images/nsfw/girl-1211435_960_720.jpg'


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


# def save_img_info(instance):
#     print(f'INFO: **************img instance have been created, saving img info now...')
#     addr = Address()
#     eval = Evaluate()
#     date = Date()
#     lm_tags = []
#     img_read = exivImg(instance.src.path)  # 登记图片路径
#     exif = img_read.read_exif()  # 读取元数据，这会返回一个字典
#     iptc = img_read.read_iptc()  # 读取元数据，这会返回一个字典
#     xmp = img_read.read_xmp()  # 读取元数据，这会返回一个字典
#     if exif:
#         print(f'INFO: exif is true ')
#         # deal with timing
#         date_str = exif['Exif.Photo.DateTimeOriginal']
#         date = set_img_date(date_str)  # return the date instance
#
#         # deal with address
#         addr.longitude_ref = exif.get('Exif.GPSInfo.GPSLongitudeRef')
#         if addr.longitude_ref:  # if have longitude info
#             addr.longitude = GPS_format(
#                 exif.get('Exif.GPSInfo.GPSLongitude'))  # exif.get('Exif.GPSInfo.GPSLongitude')
#             addr.latitude_ref = exif.get('Exif.GPSInfo.GPSLatitudeRef')
#             addr.latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude'))
#
#         addr.altitude_ref = exif.get('Exif.GPSInfo.GPSAltitudeRef')  # 有些照片无高度信息
#         if addr.altitude_ref:  # if have the altitude info
#             addr.altitude_ref = float(addr.altitude_ref)
#             addr.altitude = exif.get('Exif.GPSInfo.GPSAltitude')  # 根据高度信息，最终解析成float 格式
#             alt = addr.altitude.split('/')
#             addr.altitude = float(alt[0]) / float(alt[1])
#         print(f'instance.longitude {addr.longitude},instance.latitude {addr.latitude}')
#         addr.is_located = False
#         if addr.longitude and addr.latitude:
#             # 是否包含经纬度数据
#             addr.is_located = True
#             long_lati = GPS_to_coordinate(addr.longitude, addr.latitude)
#             addr.location, addr.district, addr.city, addr.province, addr.country = GPS_get_address(
#                 long_lati)
#
#         instance.camera_brand = exif.get('Exif.Image.Make')
#         instance.camera_model = exif.get('Exif.Image.Model')
#
#     if iptc:
#         print(f'INFO: iptc is true ')
#         instance.title = iptc.get('iptc.Application2.ObjectName')
#         instance.caption = iptc.get('Iptc.Application2.Caption')  # Exif.Image.ImageDescription
#         lm_tags = iptc.get('Iptc.Application2.Keywords')
#
#     if xmp:
#         print(f'INFO: xmp is true ')
#         instance.label = xmp.get('Xmp.xmp.Label')  # color mark
#         eval.rating = xmp.get('Xmp.xmp.Rating')
#         if eval.rating:
#             eval.rating = int(xmp.get('Xmp.xmp.Rating'))
#
#     instance.wid = instance.src.width
#     instance.height = instance.src.height
#     instance.aspect_ratio = instance.height / instance.wid
#     instance.is_exist = True
#     # instance.save()   # save the image instance, already saved during save the author
#
#     if lm_tags:
#         print(f'INFO: the lm_tags is {lm_tags}, type is {type(lm_tags)}')
#         print(f'INFO: the instance id is {instance.id}')
#         # instance.tags.set(lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
#         instance.tags.add(*lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
#
#     addr.img = instance
#     eval.img = instance
#     date.img = instance
#     addr.save()
#     eval.save()
#     date.save()


# def set_img_group(img_obj):
#     names = img_obj.faces.values_list('name', flat=True)
#     name_cnt = names.count()
#     if name_cnt > 5:
#         return
#     name_str = ','.join(names)
#     img_set = Img.objects.annotate(faces_num=Count('faces')).filter(faces_num=name_cnt)
#     for name in names:
#         if not img_set.exists():
#             break
#         img_set = img_set.filter(faces__name=name)
#     img_set.count()
#
#     rst = Category.objects.filter(type='group').filter(img__in=img_set)
#     # rst = Category.objects.filter(type = 'group').filter(img = img_set)
#     if rst.exists():
#         rst = rst.first()
#         # rst.img.add(*img_set)
#         rst.img.add(img_obj)
#     else:
#         cate_obj = Category.objects.create(name=name_str, type='group', value=name_str)
#         cate_obj.img.set(img_set)


def add_img_colors_to_category(img_obj):
    if not hasattr(img_obj, 'colors'):
        print(f'----------{img_obj.id} INFO: there is no color info in this img-------------')
        # Color fetch here later
        set_img_colors(img_obj)
        img_obj.refresh_from_db()  # refresh the result from the database since the color is checked

    img_colors = img_obj.colors.image.all()
    fore_colors = img_obj.colors.foreground.all()
    back_colors = img_obj.colors.background.all()
    for color in img_colors:
        print(color)
        cate_obj = Category.objects.filter(name=color.closest_palette_color_parent, type='img_color')  # checking whether exist this palette
        if cate_obj.exists():
            cate_obj = cate_obj.first()
        else:
            cate_obj = Category.objects.create(name=color.closest_palette_color_parent, type='img_color',
                                               value=color_palette[color.closest_palette_color_parent])
        cate_obj.img.add(img_obj)

    for color in fore_colors:
        print(color)
        cate_obj = Category.objects.filter(name=color.closest_palette_color_parent, type='fore_color')  # checking whether exist this palette
        if cate_obj.exists():
            cate_obj = cate_obj.first()
        else:
            cate_obj = Category.objects.create(name=color.closest_palette_color_parent, type='fore_color',
                                               value=color_palette[color.closest_palette_color_parent])
        cate_obj.img.add(img_obj)

    for color in back_colors:
        print(color)
        cate_obj = Category.objects.filter(name=color.closest_palette_color_parent, type='back_color')  # checking whether exist this palette
        if cate_obj.exists():
            cate_obj = cate_obj.first()
        else:
            cate_obj = Category.objects.create(name=color.closest_palette_color_parent, type='back_color',
                                               value=color_palette[color.closest_palette_color_parent])
        cate_obj.img.add(img_obj)
    print(
        f'-------------------{img_obj.id} :img colors have been added to the category database------------------------')


def add_all_img_colors_to_category():
    imgs = Img.objects.all()
    # imgs = Img.objects.filter(id__lt=425)
    for img in imgs:
        add_img_colors_to_category(img)


# img_obj = Img.objects.get(pk=431)
# face_obj = Face.objects.get(pk=625)
# face2_obj = Face.objects.get(pk=626)
# facealbum_obj = FaceAlbum.objects.get(pk=32)

# set_img_categories(img_obj)
# save_img_info(img_obj)
add_all_img_colors_to_category()
Img.objects.filter(Q(faces__name='blue')).count()
print('--------------------end---------------------------')
