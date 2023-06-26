# Generated by Django 3.2.9 on 2022-09-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face', '0007_alter_face_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facealbum',
            name='name',
            field=models.CharField(blank=True, default='unknown', help_text='请对该人脸相册进行命名', max_length=20, null=True, unique=True, verbose_name='人脸名'),
        ),
    ]