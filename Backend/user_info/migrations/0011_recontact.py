# Generated by Django 3.2.9 on 2023-08-13 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('user_info', '0010_auto_20230627_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.CharField(blank=True, choices=[(0, '客户'), (1, '供应商'), (2, '合作伙伴'), (3, '其它')], default='friend', help_text='re_from和re_to的关系', max_length=10, verbose_name='关系')),
                ('nickname', models.CharField(blank=True, help_text='re_from的真实名字', max_length=20, verbose_name='re_from的真实名字')),
                ('PyInitial', models.CharField(blank=True, help_text='re_from的拼音首字母', max_length=20, verbose_name='re_from的拼音首字母')),
                ('quanpin', models.CharField(blank=True, help_text='re_from的全拼', max_length=20, verbose_name='re_from的全拼')),
                ('conRemark', models.CharField(blank=True, help_text='re_from的备注', max_length=20, verbose_name='re_from的备注')),
                ('conRemarkPYFull', models.CharField(blank=True, help_text='re_from的备注拼音全拼', max_length=20, verbose_name='re_from的备注拼音全拼')),
                ('conRemarkPYShort', models.CharField(blank=True, help_text='re_from的备注拼音首字母', max_length=20, verbose_name='re_from的备注拼音首字母')),
                ('desc', models.TextField(blank=True, help_text='描述', verbose_name='描述')),
                ('sourceExtInfo', models.CharField(blank=True, help_text='来源扩展信息', max_length=20, verbose_name='来源扩展信息')),
                ('re_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='re_from_relations', to=settings.AUTH_USER_MODEL)),
                ('re_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='re_to_relations', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='给这位联系人打上的标签', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]