# Generated by Django 3.2.9 on 2023-12-02 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0052_auto_20231202_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colorbackground',
            old_name='color',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='colorforeground',
            old_name='color',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='colorimg',
            old_name='color',
            new_name='img',
        ),
    ]
