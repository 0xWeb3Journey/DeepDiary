# Generated by Django 3.2.9 on 2022-07-18 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_img_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='img',
            old_name='image',
            new_name='src',
        ),
    ]
