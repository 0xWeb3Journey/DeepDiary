# Generated by Django 3.2.9 on 2022-06-04 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('library', '0001_initial'),
        ('face', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='face',
            name='img',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faces', to='library.img', verbose_name='所属照片'),
        ),
    ]
