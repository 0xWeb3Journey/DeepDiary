# Generated by Django 3.2.9 on 2023-10-03 09:42

from django.db import migrations, models
import user_info.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0017_rename_image_image_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='avatar',
            field=models.ImageField(blank=True, default='sys_img/logo_lg.png', help_text='请上传图片', null=True, upload_to=user_info.models.user_upload_img, verbose_name='图片'),
        ),
        migrations.AddField(
            model_name='company',
            name='name_PyInitial',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='公司名称拼音首字母'),
        ),
    ]