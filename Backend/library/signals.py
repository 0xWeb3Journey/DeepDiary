# Create your models here.
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from pyexiv2 import Image as exivImg

from library.gps import GPS_format, GPS_to_coordinate, GPS_get_address
from library.models import Img, ImgMcs
from library.task import ImgProces


# Create your models here.


# 信号接收函数，每当新建 Image 实例时自动调用
@receiver(post_save, sender=Img)
def create_img_info(sender, instance, created, **kwargs):
    if created:
        print('Image instance have been created, deal with post_save signal')
        # img_process = ImgProces(instance=instance)
        # img_process.face_get()


# 信号接收函数，每当更新 Img 实例时自动调用
@receiver(post_save, sender=Img)
def update_img_info(sender, instance, **kwargs):
    # print(f'INFO: img instance have been updated')
    # print(f'INFO: instance is {instance}')
    # print(f'INFO: sender is {sender}')
    pass


