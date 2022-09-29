import pickle
import time
from datetime import datetime

from celery import shared_task
from django.db.models import Count
from pyexiv2 import Image as exivImg

from deep_diary.config import wallet_info
from face.models import Face
from face.task import upload_face_to_mcs
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.imagga import imagga_post
from library.models import Img, ColorBackground, Category, ImgCategory, Address, Date, Evaluate
from library.serializers import McsSerializer, McsDetailSerializer, ColorSerializer, ColorBackgroundSerializer, \
    ColorForegroundSerializer, ColorImgSerializer
from mycelery.main import app
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


# @app.task
@shared_task
def send_email(name):
    print("向%s发送邮件..." % name)
    time.sleep(5)
    print("向%s发送邮件完成" % name)
    return "ok"


# @app.task
# @shared_task
# def save_img_info(instance):
#     print(f'INFO: **************img instance have been created, saving img info now...')
#     lm_tags = []
#     img_read = exivImg(instance.src.path)  # 登记图片路径
#     exif = img_read.read_exif()  # 读取元数据，这会返回一个字典
#     iptc = img_read.read_iptc()  # 读取元数据，这会返回一个字典
#     xmp = img_read.read_xmp()  # 读取元数据，这会返回一个字典
#     if exif:
#         print(f'INFO: exif is true ')
#         instance.longitude_ref = exif.get('Exif.GPSInfo.GPSLongitudeRef')
#         if instance.longitude_ref:  # if have longitude info
#             instance.longitude = GPS_format(
#                 exif.get('Exif.GPSInfo.GPSLongitude'))  # exif.get('Exif.GPSInfo.GPSLongitude')
#             instance.latitude_ref = exif.get('Exif.GPSInfo.GPSLatitudeRef')
#             instance.latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude'))
#
#         instance.altitude_ref = exif.get('Exif.GPSInfo.GPSAltitudeRef')  # 有些照片无高度信息
#         if instance.altitude_ref:  # if have the altitude info
#             instance.altitude_ref = float(instance.altitude_ref)
#             instance.altitude = exif.get('Exif.GPSInfo.GPSAltitude')  # 根据高度信息，最终解析成float 格式
#             alt = instance.altitude.split('/')
#             instance.altitude = float(alt[0]) / float(alt[1])
#         print(f'instance.longitude {instance.longitude},instance.latitude {instance.latitude}')
#         is_located = False
#         if instance.longitude and instance.latitude:
#             # 是否包含经纬度数据
#             instance.is_located = True
#             long_lati = GPS_to_coordinate(instance.longitude, instance.latitude)
#             instance.location, instance.district, instance.city, instance.province, instance.country = GPS_get_address(
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
#         instance.rating = xmp.get('Xmp.xmp.Rating')
#         if instance.rating:
#             instance.rating = int(xmp.get('Xmp.xmp.Rating'))
#
#     # print(f"INFO: instance.src.width: {instance.src.width}")
#     # print(f"INFO: instance.src.height: {instance.src.height}")
#     instance.wid = instance.src.width
#     instance.height = instance.src.height
#     instance.aspect_ratio = instance.height / instance.wid
#     instance.is_exist = True
#     instance.save()
#
#     if lm_tags:
#         print(f'INFO: the lm_tags is {lm_tags}, type is {type(lm_tags)}')
#         print(f'INFO: the instance id is {instance.id}')
#         # time.sleep(5)  # Delays for 5 seconds. You can also use a float value.
#         instance.tags.set(lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
#         # obj = Img.objects.get(id=instance.id)
#         # obj.tags.set(lm_tags)

# @app.task
@shared_task
def upload_img_to_mcs(img):  # img = self.get_object()  # 获取详情的实例对象
    if not hasattr(img, 'mcs'):  # 判断是否又对应的mcs存储

        data = upload_file_pay(wallet_info, img.src.path)
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


@shared_task
def upload_to_mcs():
    print('-----------------start upload all the imgs to mcs-----------------')
    imgs = Img.objects.filter(mcs__isnull=True)
    for (img_idx, img) in enumerate(imgs):
        print(f'--------------------INFO: This is img{img_idx}: {img.id} ---------------------')
        upload_img_to_mcs(img)
    print('------------all the imgs have been uploaded to mcs----------------')

    print('-----------------start upload all the faces to mcs-----------------')
    fcs = Face.objects.filter(mcs__isnull=True)
    for (fc_idx, fc) in enumerate(fcs):
        print(f'--------------------NFO: This is face{fc_idx}: {fc.name}---------------------')
        upload_face_to_mcs(fc)
    print('------------all the faces have been uploaded to mcs----------------')

    print('----end----')


@shared_task
def set_img_tags(img_obj):
    img_path = img_obj.src.path
    endpoint = 'tags'
    tagging_query = {
        'verbose': False,
        'language': 'en',
        'threshold': 25,
    }

    response = imagga_post(img_path, endpoint, tagging_query)
    # with open("tags.txt", 'wb') as f:  # store the result object, which will helpful for debugging
    #     pickle.dump(response, f)
    #
    # with open("tags.txt", 'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
    #     response = pickle.load(f)

    if 'result' in response:
        tags = response['result']['tags']
        tag_list = []

        for tag in tags:
            tag_list.append(tag['tag']['en'])

        # img_obj.tags.set(tag_list)
        img_obj.tags.add(*tag_list)
        print(f'--------------------{img_obj.id} :tags have been store to the database---------------------------')


@shared_task
def set_all_img_tags():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_tags(img)


@shared_task
def set_img_colors(img_obj):
    # this is through post method to get the tags. mainly is used for local img
    img_path = img_obj.src.path
    endpoint = 'colors'
    # color_query = {                 #  if it is necessary, we could add the query info here
    #     'verbose': False,
    #     'language': False,
    #     'threshold': 25.0,
    # # }

    response = imagga_post(img_path, endpoint)
    # print(response)
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


@shared_task
def set_all_img_colors():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_colors(img)


@shared_task
def set_img_categories(img_obj):
    img_path = img_obj.src.path
    endpoint = 'categories/personal_photos'

    response = imagga_post(img_path, endpoint)
    # with open("categories.txt", 'wb') as f:  # store the result object, which will helpful for debugging
    #     pickle.dump(response, f)

    # with open("categories.txt",
    #           'rb') as f:  # during the debug, we could using the local stored object. since the api numbers is limited
    #     response = pickle.load(f)

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

        print(img_cate_list)
        ImgCategory.objects.bulk_create(img_cate_list)

        # img_obj.categories.add(*categories_list, through_defaults=confidence_list)

        print(
            f'--------------------{img_obj.id} :categories have been store to the database---------------------------')


@shared_task
def set_all_img_categories():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_categories(img)


def set_img_date(date_str):  # '%Y:%m:%d %H:%M:%S'
    date = Date()
    if not date_str:
        date_str = '1970:01:01 00:00:00'

    tt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

    date.capture_date = tt.strftime("%Y-%m-%d")
    date.capture_time = tt.strftime("%H:%M:%S")
    date.year = str(tt.year).rjust(2, '0')
    date.month = str(tt.month).rjust(2, '0')
    date.day = str(tt.day).rjust(2, '0')

    if tt.weekday() < 5:
        date.is_weekend = False
    else:
        date.is_weekend = True
    if 0 < tt.hour < 5:
        date.earthly_branches = 0  # 这个判断需要后续完善，可以直接把字符串格式化后，再判读时间是否属于朝九晚五
    elif 5 < tt.hour < 8:
        date.earthly_branches = 1
    elif 8 < tt.hour < 17:
        date.earthly_branches = 2
    elif 17 < tt.hour < 21:
        date.earthly_branches = 3
    else:
        date.earthly_branches = 4

    return date


@shared_task
def save_img_info(instance):
    print(f'INFO: **************img instance have been created, saving img info now...')
    addr = Address()
    eval = Evaluate()
    date = Date()
    lm_tags = []
    img_read = exivImg(instance.src.path)  # 登记图片路径
    exif = img_read.read_exif()  # 读取元数据，这会返回一个字典
    iptc = img_read.read_iptc()  # 读取元数据，这会返回一个字典
    xmp = img_read.read_xmp()  # 读取元数据，这会返回一个字典
    if exif:
        print(f'INFO: exif is true ')
        # deal with timing
        date_str = exif['Exif.Photo.DateTimeOriginal']
        date = set_img_date(date_str)  # return the date instance

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
        print(f'instance.longitude {addr.longitude},instance.latitude {addr.latitude}')
        addr.is_located = False
        if addr.longitude and addr.latitude:
            # 是否包含经纬度数据
            addr.is_located = True
            long_lati = GPS_to_coordinate(addr.longitude, addr.latitude)
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
    # instance.save()   # save the image instance, already saved during save the author

    if lm_tags:
        print(f'INFO: the lm_tags is {lm_tags}, type is {type(lm_tags)}')
        print(f'INFO: the instance id is {instance.id}')
        # instance.tags.set(lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
        instance.tags.add(*lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联

    addr.img = instance
    eval.img = instance
    date.img = instance
    addr.save()
    eval.save()
    date.save()
    print(
        f'--------------------{instance.id} :img infos have been store to the database---------------------------')


@shared_task
def save_all_img_info():
    imgs = Img.objects.all()
    for img in imgs:
        save_img_info(img)


@shared_task
def set_img_group(img_obj):
    names = img_obj.faces.values_list('name', flat=True)
    name_cnt = names.count()
    if name_cnt < 2:  # if faces biger then 5, then break
        print(
            f'--------------------{img_obj.id} :too less faces in the img, skip for this---------------------------')
        return
    if name_cnt > 5:  # if faces biger then 5, then break
        print(
            f'--------------------{img_obj.id} :too many faces in the img, skip for this---------------------------')
        return
    name_str = ','.join(names)
    name_str = name_str[0:29]  # the name couldn't be too long
    img_set = Img.objects.annotate(faces_num=Count('faces')).filter(faces_num=name_cnt)
    for name in names:
        if not img_set.exists():
            print(f'--------------------{img_obj.id} :the filter result is none--------------------')
            break
        img_set = img_set.filter(faces__name=name)
    print(f'img_set number is: {img_set.count()}')

    rst = Category.objects.filter(type='group').filter(img__in=img_set)
    # rst = Category.objects.filter(type = 'group').filter(img = img_set)
    if rst.exists():
        rst = rst.first()
        # rst.img.add(*img_set)
        rst.img.add(img_obj)
    else:
        cate_obj = Category.objects.create(name=name_str, type='group', value=name_str)
        cate_obj.img.set(img_set)
    print(
        f'--------------------{img_obj.id} :img group have been store to the database---------------------------')


@shared_task
def set_all_img_group():
    imgs = Img.objects.all()
    for img in imgs:
        set_img_group(img)


@shared_task
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


@shared_task
def add_all_img_colors_to_category():
    imgs = Img.objects.filter(id__lt=425)
    for img in imgs:
        add_img_colors_to_category(img)
