# Generated by Django 3.2.9 on 2023-06-23 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0008_auto_20230622_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='feat',
            new_name='embedding',
        ),
    ]