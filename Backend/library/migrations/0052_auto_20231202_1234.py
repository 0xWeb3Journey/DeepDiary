# Generated by Django 3.2.9 on 2023-12-02 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0051_auto_20231126_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorbackground',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cbacks', to='library.img', verbose_name='BackgroundColor'),
        ),
        migrations.AlterField(
            model_name='colorforeground',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cfores', to='library.img', verbose_name='ColorForeground'),
        ),
        migrations.AlterField(
            model_name='colorimg',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cimgs', to='library.img', verbose_name='ColorImg'),
        ),
    ]
