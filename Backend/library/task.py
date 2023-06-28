import bisect
import pickle
import random
import string
from datetime import datetime
from io import BytesIO

import cv2
import numpy as np
import pyexiv2
from PIL import Image
from celery import shared_task
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction, IntegrityError
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

from deep_diary.settings import cfg, calib
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.imagga import imagga_get
from library.models import Img, Category, ImgCategory, Face, \
    FaceLandmarks3D, FaceLandmarks2D, Kps
from library.serializers import McsDetailSerializer, ColorSerializer, ColorBackgroundSerializer, \
    ColorForegroundSerializer, ColorImgSerializer, FaceSerializer
from user_info.models import Profile
from utils.mcs_storage import upload_file_pay

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


def set_img_date(date, date_str):  # 1. date instance, 2 '%Y:%m:%d %H:%M:%S'
    if not date_str:
        date_str = '1970:01:01 00:00:00'
    tt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    date.capture_date = tt.strftime("%Y-%m-%d")
    date.capture_time = tt.strftime("%H:%M:%S")
    date.year = str(tt.year).rjust(2, '0')
    date.month = str(tt.month).rjust(2, '0')
    date.day = str(tt.day).rjust(2, '0')
    date.is_weekend = False if tt.weekday() < 5 else True
    date.earthly_branches = bisect.bisect_right(calib['hour_slot'], tt.hour) - 1
    print(date.earthly_branches, type(date.earthly_branches))
    return date


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


# @shared_task
def set_img_info(instance, f_path=None):
    # if f_path is None:
    #     print(f'the f_path is not available')
    #     return
    if instance.stats.is_get_info:  # already fetch the info
        print('this image already got the basic info like date, address and other exif info')
        return
    print(f'INFO: **************img instance have been created, saving img info now...')
    addr = instance.address
    eval = instance.evaluates
    date = instance.dates
    stat = instance.stats
    lm_tags = []
    img_read = pyexiv2.Image(f_path)  # 登记图片路径
    # img_read = pyexiv2.Image(r'd:\test images\IMG_20210928_195317.jpg')  # 登记图片路径
    exif = img_read.read_exif()  # 读取元数据，这会返回一个字典
    iptc = img_read.read_iptc()  # 读取元数据，这会返回一个字典
    xmp = img_read.read_xmp()  # 读取元数据，这会返回一个字典
    if exif:
        print(f'INFO: exif is true ')
        # deal with timing
        date_str = exif['Exif.Photo.DateTimeOriginal']
        date = set_img_date(date, date_str)  # return the date instance

        # deal with address
        addr.longitude_ref = exif.get('Exif.GPSInfo.GPSLongitudeRef')
        if addr.longitude_ref:  # if have longitude info
            addr.longitude = GPS_format(
                exif.get('Exif.GPSInfo.GPSLongitude'))  # exif.get('Exif.GPSInfo.GPSLongitude')
            addr.latitude_ref = exif.get('Exif.GPSInfo.GPSLatitudeRef')
            addr.latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude'))

        addr.altitude_ref = exif.get('Exif.GPSInfo.GPSAltitudeRef')  # 有些照片无高度信息
        if addr.altitude_ref:  # if have the altitude info
            addr.altitude_ref = float(addr.altitude_ref)
            addr.altitude = exif.get('Exif.GPSInfo.GPSAltitude')  # 根据高度信息，最终解析成float 格式
            alt = addr.altitude.split('/')
            addr.altitude = float(alt[0]) / float(alt[1])
        addr.is_located = False
        if addr.longitude and addr.latitude:
            # 是否包含经纬度数据
            addr.is_located = True
            long_lati = GPS_to_coordinate(addr.longitude, addr.latitude)
            # TODO: need update the lnglat after transform the GPS info
            addr.longitude = round(long_lati[0], 6)  # only have Only 6 digits of precision for AMAP
            addr.latitude = round(long_lati[1], 6)
            # print(f'instance.longitude {addr.longitude},instance.latitude {addr.latitude}')
            long_lati = f'{long_lati[0]},{long_lati[1]}'  # change to string

            addr.location, addr.district, addr.city, addr.province, addr.country = GPS_get_address(
                long_lati)

        instance.camera_brand = exif.get('Exif.Image.Make')
        instance.camera_model = exif.get('Exif.Image.Model')

    if iptc:
        print(f'INFO: iptc is true ')
        instance.title = iptc.get('iptc.Application2.ObjectName')
        instance.caption = iptc.get('Iptc.Application2.Caption')  # Exif.Image.ImageDescription
        lm_tags = iptc.get('Iptc.Application2.Keywords')

    if xmp:
        print(f'INFO: xmp is true ')
        instance.label = xmp.get('Xmp.xmp.Label')  # color mark
        eval.rating = int(xmp.get('Xmp.xmp.Rating', 0))
        # if eval.rating:
        #     eval.rating = int(xmp.get('Xmp.xmp.Rating'))

    instance.wid = instance.src.width
    instance.height = instance.src.height
    instance.aspect_ratio = instance.height / instance.wid
    instance.is_exist = True
    instance.save()  # save the image instance, already saved during save the author

    if lm_tags:
        print(f'INFO: the lm_tags is {lm_tags}, type is {type(lm_tags)}')
        print(f'INFO: the instance id is {instance.id}')
        # instance.tags.set(lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
        instance.tags.add(*lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联

    stat.is_publish = True
    stat.is_get_info = True

    #  mask this since already bind the img instance in view--》create
    # addr.img = instance
    # eval.img = instance
    # date.img = instance
    # stat.img = instance
    addr.save()
    eval.save()
    date.save()
    stat.save()
    print(
        f'--------------------{instance.id} :img infos have been store to the database---------------------------')


# @app.task
# @shared_task
def set_img_mcs(img):  # img = self.get_object()  # 获取详情的实例对象
    if not hasattr(img, 'mcs'):  # 判断是否又对应的mcs存储

        data = upload_file_pay(cfg['wallet_info'], img.src.path)
        # 调用序列化器进行反序列化验证和转换
        data.update(id=img.id)
        print(data)
        serializer = McsDetailSerializer(data=data)
        # 当验证失败时,可以直接通过声明 raise_exception=True 让django直接跑出异常,那么验证出错之后，直接就再这里报错，程序中断了就

        result = serializer.is_valid(raise_exception=True)
        print(serializer.errors)  # 查看错误信息

        # 获取通过验证后的数据
        print(serializer.validated_data)  # form -- clean_data
        # 保存数据
        mcs_obj = serializer.save()

        msg = 'success to make a copy into mac, the file_upload_id is %d' % mcs_obj.file_upload_id

    else:
        msg = 'there is already have mac info related to this img: file id is %d' % img.mcs.file_upload_id

    print(msg)


# @shared_task
def set_img_tags(img_obj):
    if img_obj.stat.is_auto_tag:  # already fetch the info
        print('this image already auto tagged')
        return
    # img_path = img_obj.src.path  # oss have no path attribute
    img_path = img_obj.src.url
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
    print(response)

    if 'result' in response:
        tags = response['result']['tags']
        tag_list = []

        for tag in tags:
            tag_list.append(tag['tag']['en'])

        # img_obj.tags.set(tag_list)
        img_obj.tags.add(*tag_list)

        img_obj.stat.is_auto_tag = True
        img_obj.stat.save()

        print(f'--------------------{img_obj.id} :tags have been store to the database---------------------------')


# @shared_task
def set_img_colors(img_obj):
    if img_obj.stat.is_get_color:  # already fetch the info
        print('this image already got the color')
        return
    # this is through post method to get the tags. mainly is used for local img
    # img_path = img_obj.src.path  # local image
    img_path = img_obj.src.url  # web image
    endpoint = 'colors'
    # color_query = {                 #  if it is necessary, we could add the query info here
    #     'verbose': False,
    #     'language': False,
    #     'threshold': 25.0,
    # # }

    # response = imagga_post(img_path, endpoint)
    response = imagga_get(img_path, endpoint)

    with open("colors.txt", 'wb') as f:  # store the result object, which will helpful for debugging
        pickle.dump(response, f)

    # with open("colors.txt", 'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
    #     response = pickle.load(f)

    print(response)

    if response['status']['type'] != 'success':
        return []

    if 'result' in response:
        colors = response['result'][endpoint]
        background_colors = colors['background_colors']
        foreground_colors = colors['foreground_colors']
        image_colors = colors['image_colors']

        # print(colors)

        # 调用序列化器进行反序列化验证和转换
        colors.update(img=img_obj.id)  # bind the one to one field image info
        if not hasattr(img_obj, 'colors'):  # if img_obj have no attribute of colors, then create it
            print('no colors object existed')
            serializer = ColorSerializer(data=colors)
        else:  # if img_obj already have attribute of colors, then updated it
            print('colors object already existed')
            serializer = ColorSerializer(img_obj.colors, data=colors)
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

        img_obj.stat.is_get_color = True
        img_obj.stat.save()
        print(f'--------------------{img_obj.id} :colors have been store to the database---------------------------')


# @shared_task
def set_img_categories(img_obj):
    if img_obj.stat.is_get_cate:  # already fetch the info
        print('this image already got the categories')
        return
    # img_path = img_obj.src.path  # local image
    img_path = img_obj.src.url  # web image
    endpoint = 'categories/personal_photos'

    # response = imagga_post(img_path, endpoint)
    response = imagga_get(img_path, endpoint)
    # with open("categories.txt", 'wb') as f:  # store the result object, which will helpful for debugging
    #     pickle.dump(response, f)

    # with open("categories.txt",
    #           'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
    #     response = pickle.load(f)
    print(response)

    if 'result' in response:
        categories = response['result']['categories']
        categories_list = []
        img_cate_list = []
        data = {}

        for item in categories:
            # obj = Category(name=item['name']['en'], confidence=item['confidence'])
            checkd_obj = Category.objects.filter(name=item['name']['en'])
            if checkd_obj.exists():
                # print(f'--------------------categories have already existed---------------------------')
                # return
                obj = checkd_obj.first()
            else:
                obj = Category.objects.create(name=item['name']['en'])

            if ImgCategory.objects.filter(img=img_obj, category=obj).exists():
                print(f'--------------------ImgCategory have already existed---------------------------')
                continue
            item = ImgCategory(img=img_obj, category=obj, confidence=item['confidence'])
            img_cate_list.append(item)
            categories_list.append(obj)

        ImgCategory.objects.bulk_create(img_cate_list)

        # img_obj.categories.add(*categories_list, through_defaults=confidence_list)
        img_obj.stat.is_get_cate = True
        img_obj.stat.save()
        print(
            f'--------------------{img_obj.id} :categories have been store to the database---------------------------')


# @shared_task
def add_img_face_to_category(img_obj):
    if not hasattr(img_obj, 'faces'):
        print(f"\033[1;32m ----------{img_obj.id} INFO: there is no faces info in this img--------- \033[0m")
        return
    # check whether has the unknown face, unknown means unnamed
    fc_unknown_obj = img_obj.faces.filter(name__startswith='unknown')
    if fc_unknown_obj.exists():
        print(f'\033[1;32m ----------{img_obj.id} INFO: there is unknown face in this img---------- \033[0m')
        return
    names = img_obj.faces.order_by('name').values_list('name', flat=True)
    name_cnt = names.count()
    name_str = 'no face'  # default
    if name_cnt <= 1:
        # print(
        #     f'----------------{img_obj.id} :return-->this is the single or no face-----------------------')
        return
    elif 1 < name_cnt <= 6:  # if faces biger then 1, small then 6
        # print(
        # f'----------------{img_obj.id} :found the face group-----------------------')
        name_str = ','.join(names)
    elif name_cnt > 6:  # if faces biger then 5, then break
        # print(
        #     f'----------------{img_obj.id} :too many faces in the img-----------------------')
        name_str = 'group face'

    rst = Category.objects.filter(type='group', name=name_str)

    if rst.exists():
        rst = rst.first()
        # rst.img.add(*img_set)
        print(f"\033[1;32m --------{img_obj.id} :img group have been added to the database------------ \033[0m")
    else:
        rst = Category.objects.create(name=name_str, type='group', numeric_value=name_cnt, avatar=img_obj.src)
        print(f"\033[1;32m --------{img_obj.id} :img group have been created to the database---------- \033[0m")
        # rst.img.set(img_set)
    rst.img.add(img_obj)


# @shared_task
def add_img_addr_to_category(img_obj):
    if not hasattr(img_obj, 'address'):
        print(f'\033[1;32m ----------{img_obj.id} INFO: there is no address info in this img--------- \033[0m')
        return
    city = img_obj.address.city
    if city is None:
        # print(f'----------------{img_obj.id} :there is no address info in this img---------------------')
        city = 'No GPS'

    rst, created = Category.objects.get_or_create(name=city, type='address')

    rst.img.add(img_obj)
    if created:
        print(f'\033[1;32m --------{img_obj.id} :img address have been created to the database-------- \033[0m')
    else:
        print(f'\033[1;32m --------{img_obj.id} :img address have been added to the database---------- \033[0m')


# @shared_task
def add_img_colors_to_category(img_obj):
    if not hasattr(img_obj, 'colors'):
        print(f'----------{img_obj.id} INFO: there is no color info in this img---------')
        return
        # Color fetch here later
        # set_img_colors(img_obj)
        # img_obj.refresh_from_db()  # refresh the result from the database since the color is checked

    img_colors = img_obj.colors.image.all()
    fore_colors = img_obj.colors.foreground.all()
    back_colors = img_obj.colors.background.all()
    for color in img_colors:
        cate_obj = Category.objects.filter(name=color.closest_palette_color_parent,
                                           type='img_color')  # checking whether exist this palette
        if cate_obj.exists():
            cate_obj = cate_obj.first()
            print(f'\033[1;32m --------{img_obj.id} :img colors have been added to the category database---- \033[0m')
        else:
            cate_obj = Category.objects.create(name=color.closest_palette_color_parent, type='img_color',
                                               value=color_palette[color.closest_palette_color_parent])
            print(f'\033[1;32m --------{img_obj.id} :img colors have been created to the category database---- \033[0m')
        cate_obj.img.add(img_obj)

    for color in fore_colors:
        cate_obj = Category.objects.filter(name=color.closest_palette_color_parent,
                                           type='fore_color')  # checking whether exist this palette
        if cate_obj.exists():
            cate_obj = cate_obj.first()
            print(f'\033[1;32m --------{img_obj.id} :fore colors have been added to the category database---- \033[0m')
        else:
            cate_obj = Category.objects.create(name=color.closest_palette_color_parent, type='fore_color',
                                               value=color_palette[color.closest_palette_color_parent])
            print(
                f'\033[1;32m --------{img_obj.id} :fore colors have been created to the category database---- \033[0m')
        cate_obj.img.add(img_obj)

    for color in back_colors:
        cate_obj = Category.objects.filter(name=color.closest_palette_color_parent,
                                           type='back_color')  # checking whether exist this palette
        if cate_obj.exists():
            cate_obj = cate_obj.first()
            print(f'\033[1;32m --------{img_obj.id} :back colors have been added to the category database---- \033[0m')
        else:
            cate_obj = Category.objects.create(name=color.closest_palette_color_parent, type='back_color',
                                               value=color_palette[color.closest_palette_color_parent])
            print(
                f'\033[1;32m --------{img_obj.id} :back colors have been created to the category database---- \033[0m')
        cate_obj.img.add(img_obj)


@shared_task
def img_process(instance):
    set_img_info(instance)  # if this add the delay function, this function will be processed by celery
    set_img_tags(instance)  # if this add the delay function, this function will be processed by celery
    set_img_colors(instance)  # if this add the delay function, this function will be processed by celery
    set_img_categories(instance)  # if this add the delay function, this function will be processed by celery
    # set_img_mcs(instance)
    # save_insight_faces(instance)  # 保存insightface识别结果

    # instance.refresh_from_db()
    #
    # add_img_face_to_category(instance)
    # add_img_addr_to_category(instance)
    # add_img_colors_to_category(instance)


# @shared_task
def set_all_img_mcs():
    print('-----------------start upload all the imgs to mcs-----------------')
    imgs = Img.objects.filter(mcs__isnull=True)
    for (img_idx, img) in enumerate(imgs):
        print(f'--------------------INFO: This is img{img_idx}: {img.id} ---------------------')
        set_img_mcs(img)
    print('------------all the imgs have been uploaded to mcs----------------')

    print('-----------------start upload all the faces to mcs-----------------')
    # fcs = Face.objects.filter(mcs__isnull=True)
    # for (fc_idx, fc) in enumerate(fcs):
    #     print(f'--------------------NFO: This is face{fc_idx}: {fc.name}---------------------')
    #     set_face_mcs(fc)
    print('------------all the faces have been uploaded to mcs----------------')

    print('----end----')


# @shared_task
def set_all_img_tags():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_tags(img)


# @shared_task
def set_all_img_colors():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_colors(img)


# @shared_task
def set_all_img_categories():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_categories(img)


# @shared_task
def set_all_img_info():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_info(img)


@shared_task
def add_all_img_face_to_category():
    imgs = Img.objects.all()
    for img in imgs:
        add_img_face_to_category(img)


@shared_task
def add_all_img_addr_to_category():
    imgs = Img.objects.all()
    for img in imgs:
        add_img_addr_to_category(img)


@shared_task
def add_all_img_colors_to_category():
    imgs = Img.objects.all()
    for img in imgs:
        add_img_colors_to_category(img)


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
        self.path = path
        if instance:
            self.instance = instance
            self.path = instance.src.name
        self.procedure = procedure

    #     # img_path = img_obj.src.path  # local image
    #     img_path = img.src.url  # web image
    #
    #     # req_img = cv.imread(img_path)  # 自己用openCV进行读取, not useful for url image

    def read(self, image_path):
        """
        image_path： 图片路径， 可以是本地的，也可以是云存储的, 相对于 media 文件夹的路径
        image_content: 二进制文件流
        """
        # 读取图片
        image_file = self.instance.src.open()  # 方式一：读取本地或网络图片
        # image_file = default_storage.open(image_path)  # 方式二：读取本地或网络图片
        image_content = image_file.read()
        image_file.close()
        return image_content

    def exif_info_get(self, f_path=None):
        # 获取图片的exif信息,并分别保存成5个字典，
        #     img = instance
        #     addr = instance.address
        #     eval = instance.evaluates
        #     date = instance.dates
        #     stat = instance.stats
        if f_path is None:
            print(f'the f_path is not available')
            return
        if self.instance.stats.is_get_info:  # already fetch the info
            print('this image already got the basic info like date, address and other exif info')
            return
        print(f'INFO: **************img instance have been created, saving img info now...')

        lm_tags = []
        img_read = pyexiv2.Image(f_path)  # 登记图片路径
        exif = img_read.read_exif()  # 读取元数据，这会返回一个字典
        iptc = img_read.read_iptc()  # 读取元数据，这会返回一个字典
        xmp = img_read.read_xmp()  # 读取元数据，这会返回一个字典


        img = {
            ...,
        }
        addr = {
            ...,
        }
        eval = {
            ...,
        }
        date = {
            ...,
        }
        stat = {
            ...,
        }
        pass

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
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def face_crop(self, image, bbox):
        """
        image: 已经打开的图片数组
        bbox: 人脸框, 格式为[x左上, y左上, wid, height]
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

    def face_recognition(self, embedding):  # 'instance', serializers
        profile = None
        face_score = 0
        # 1. 提取出Profile模型中所有embedding，记作embeddings，并进行转换
        embeddings = Profile.objects.values_list('embedding', flat=True)
        embeddings = [np.frombuffer(embedding, dtype=np.float16) for embedding in embeddings if embedding]

        # 转换为矩阵形式进行相似度计算
        embeddings_matrix = np.stack(embeddings)
        print(embeddings_matrix.shape)
        print(embedding.reshape(1, -1).shape)
        similarity_scores = cosine_similarity(embedding.reshape(1, -1), embeddings_matrix)

        # 找到最大相似度对应的索引
        max_similarity_index = np.argmax(similarity_scores)
        max_similarity_score = similarity_scores[0, max_similarity_index]

        print(similarity_scores, max_similarity_index, max_similarity_score)

        # 如果top1相似度>0.4，则更新profile和face_score
        if max_similarity_score > calib['face']['reco_threshold']:
            profile = Profile.objects.all()[int(max_similarity_index)]
            face_score = max_similarity_score

        if profile:
            print(f'INFO: recognition result: {profile}--', face_score)
        else:
            print(f'INFO: recognition result: unknown--', face_score)

        return profile, face_score

    def face_get(self, save_type='instance'):  # 'instance', serializers
        #  判断当前实例是否已经执行过人脸识别，如果是，直接打印相关信息并返回
        if self.instance.stats.is_face:
            print('face already exist')
            return
        self.face_init()
        image_content = self.read(self.path)
        image_content_obj = BytesIO(image_content)

        np_array = np.frombuffer(image_content_obj.getvalue(), np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        faces = self.app.get(image)

        image_pil = Image.open(image_content_obj)

        for face in faces:
            pose = face.pose.astype(np.float16)
            bbox = np.round(face.bbox).astype(np.int16)
            # 人脸识别---->profile
            # 根据name找到profile对象
            profile, face_score = self.face_recognition(face.normed_embedding)

            if save_type == 'instance':
                fc = {
                    'img': self.instance,
                    'profile': profile,
                    'det_score': face.det_score,
                    'face_score': face_score,
                    'is_confirmed': True if face_score > 0.8 else False,
                    'src': self.face_crop(image_pil, bbox),  # 需要对src进行赋值
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
        stats = self.instance.stats
        stats.is_face = True
        stats.save()
        return faces

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
        if profile:
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
                fc_instance.profile = profile
                fc_instance.save()
        else:
            try:
                # 创建一个新用户profile对象，设定默认密码为666，加密保存，User中is_active设置为0， username设置成name，
                # 如果username已经存在相同字段，则在name后面增加4位随机数，再次创建保存
                username = name
                while Profile.objects.filter(username=username).exists():
                    # 生成4位随机数，并与name拼接
                    random_suffix = str(random.randint(1000, 9999))
                    username = f'{name}{random_suffix}'

                profile = Profile.objects.create_user(username=username, password='deep-diary', is_active=0, name=name,
                                                      embedding=fc_instance.embedding)

                fc_instance.profile = profile
                fc_instance.save()
                print(f'INFO: success created a new profile: {profile.name}')

            except IntegrityError:
                print('ERROR: Failed to create a new profile. IntegrityError occurred.')
        return profile, fc_instance
