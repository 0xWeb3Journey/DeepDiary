# Create your models here.
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from pyexiv2 import Image as exivImg

from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.models import Img, Mcs


# Create your models here.


# 信号接收函数，每当新建 Image 实例时自动调用
@receiver(post_save, sender=Img)
def create_img_info(sender, instance, created, **kwargs):
    if created:
        print('create mcs instance')
        Mcs.objects.create(img=instance)
    #     save_img_info(instance)


# 信号接收函数，每当更新 Img 实例时自动调用
@receiver(post_save, sender=Img)
def update_img_info(sender, instance, **kwargs):
    # print(f'INFO: img instance have been updated')
    # print(f'INFO: instance is {instance}')
    # print(f'INFO: sender is {sender}')
    pass


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

