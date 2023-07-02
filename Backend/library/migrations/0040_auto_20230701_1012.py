# Generated by Django 3.2.9 on 2023-07-01 02:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0039_auto_20230624_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='numeric_value',
        ),
        migrations.RemoveField(
            model_name='category',
            name='type',
        ),
        migrations.RemoveField(
            model_name='category',
            name='value',
        ),
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='首次创建的时间', verbose_name='首次创建的时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, help_text='用于用户定义描述', null=True, verbose_name='分类描述'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_delete',
            field=models.BooleanField(default=False, help_text='是否删除', verbose_name='是否删除'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_leaf',
            field=models.BooleanField(default=False, help_text='是否叶子节点', verbose_name='是否叶子节点'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_root',
            field=models.BooleanField(default=False, help_text='是否根节点', verbose_name='是否根节点'),
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='logic',
            field=models.TextField(blank=True, help_text='用于用户定义逻辑', null=True, verbose_name='分类逻辑'),
        ),
        migrations.AddField(
            model_name='category',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='library.category'),
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='最后更新的时间', verbose_name='最后更新的时间'),
        ),
    ]
