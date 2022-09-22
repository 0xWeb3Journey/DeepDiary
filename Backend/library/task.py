import pickle
import time

from celery import shared_task
from pyexiv2 import Image as exivImg

from deep_diary.config import wallet_info
from face.models import Face
from face.task import upload_face_to_mcs
from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.imagga import imagga_post
from library.models import Img, ColorBackground, Category, ImgCategory
from library.serializers import McsSerializer, McsDetailSerializer, ColorSerializer, ColorBackgroundSerializer, \
    ColorForegroundSerializer, ColorImgSerializer
from mycelery.main import app
from utils.mcs_storage import upload_file_pay


# @app.task
@shared_task
def send_email(name):
    print("向%s发送邮件..." % name)
    time.sleep(5)
    print("向%s发送邮件完成" % name)
    return "ok"


# @app.task
@shared_task
def save_img_info(instance):
    print(f'INFO: **************img instance have been created, saving img info now...')
    lm_tags = []
    img_read = exivImg(instance.src.path)  # 登记图片路径
    exif = img_read.read_exif()  # 读取元数据，这会返回一个字典
    iptc = img_read.read_iptc()  # 读取元数据，这会返回一个字典
    xmp = img_read.read_xmp()  # 读取元数据，这会返回一个字典
    if exif:
        print(f'INFO: exif is true ')
        instance.longitude_ref = exif.get('Exif.GPSInfo.GPSLongitudeRef')
        if instance.longitude_ref:  # if have GPS data
            instance.longitude = GPS_format(
                exif.get('Exif.GPSInfo.GPSLongitude'))  # exif.get('Exif.GPSInfo.GPSLongitude')
            instance.latitude_ref = exif.get('Exif.GPSInfo.GPSLatitudeRef')
            instance.latitude = GPS_format(exif.get('Exif.GPSInfo.GPSLatitude'))

        instance.altitude_ref = exif.get('Exif.GPSInfo.GPSAltitudeRef')  # 有些照片无高度信息
        if instance.altitude_ref:  # if have the altitude info
            instance.altitude_ref = float(instance.altitude_ref)
            instance.altitude = exif.get('Exif.GPSInfo.GPSAltitude')  # 根据高度信息，最终解析成float 格式
            alt = instance.altitude.split('/')
            instance.altitude = float(alt[0]) / float(alt[1])
        print(f'instance.longitude {instance.longitude},instance.latitude {instance.latitude}')
        is_located = False
        if instance.longitude and instance.latitude:
            # 是否包含经纬度数据
            instance.is_located = True
            long_lati = GPS_to_coordinate(instance.longitude, instance.latitude)
            instance.location, instance.district, instance.city, instance.province, instance.country = GPS_get_address(
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
        instance.rating = xmp.get('Xmp.xmp.Rating')
        if instance.rating:
            instance.rating = int(xmp.get('Xmp.xmp.Rating'))

    # print(f"INFO: instance.src.width: {instance.src.width}")
    # print(f"INFO: instance.src.height: {instance.src.height}")
    instance.wid = instance.src.width
    instance.height = instance.src.height
    instance.aspect_ratio = instance.height / instance.wid
    instance.is_exist = True
    instance.save()

    if lm_tags:
        print(f'INFO: the lm_tags is {lm_tags}, type is {type(lm_tags)}')
        print(f'INFO: the instance id is {instance.id}')
        # time.sleep(5)  # Delays for 5 seconds. You can also use a float value.
        instance.tags.set(lm_tags)  # 这里一定要在实例保存后，才可以设置外键，不然无法进行关联
        # obj = Img.objects.get(id=instance.id)
        # obj.tags.set(lm_tags)


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

        img_obj.tags.set(tag_list)
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
