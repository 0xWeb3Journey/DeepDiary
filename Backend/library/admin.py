from django.contrib import admin

# Register your models here.
from library.models import Img, Mcs

admin.site.register([Mcs, Img])  # 把这个图像表注册到管理后台中
