# stat_operation.py
# force on dealing with Stat model

from library.models import Stat

from django.db import models

from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class StatOperation(BaseOperation):
    def __init__(self, img_instance=None):
        super().__init__(Stat, img_instance)
        self.tasks = ['exif', 'face', 'tag', 'color', 'category', 'clip_classification', 'feature', 'caption']
        self.stats, _ = self.model.objects.get_or_create(img=self.img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        for key, value in data.items():
            self.update_stats_flag(key, value)

    def is_process_needed(self, processor_type, force=False):
        """
        检查是否需要处理数据库保存操作。
        """
        # 判断processor_type是否有效
        if processor_type not in self.tasks:
            print(f"Invalid processor type '{processor_type}'.")
            return False
        # 判断是否需要处理
        flag_field = self._construct_flag_field(processor_type)
        if force or not getattr(self.stats, flag_field, False):
            # setattr(self.stats, flag_field, True)  # 相关处理后再设置标志位
            # self.stats.save()
            return True
        print(f"{flag_field} already processed for img {self.img_instance.id}. Set force=True to override.")
        return False

    # @trace_function
    def update_stats_flag(self, processor_type, value) -> None:
        """
        更新Img实例的Stat的对应标志位。
        """
        flag_field = self._construct_flag_field(processor_type)
        setattr(self.stats, flag_field, value)
        self.stats.save()

    def _construct_flag_field(self, processor_type):
        """
        构造标志字段名称。
        """
        return f'is_get_{processor_type}'
