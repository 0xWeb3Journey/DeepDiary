# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver

from library.models import Img


# Create your models here.


# 信号接收函数，每当新建 Image 实例时自动调用
@receiver(post_save, sender=Img)
def img_post_save_process(sender, instance, created, **kwargs):
    if created:
        print('Image instance have been created, deal with post_save signal')
        if hasattr(instance, 'stats'):
            print(f'INFO: stats is already created!')
        else:
            print(f'INFO: stats is not created, create it!')

    else:
        print('Image instance have been updated, deal with post_save signal')




