# img_operation.py
# force on dealing with Img model
from datetime import datetime

from django.db import models

from library.models import Img, Date
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class DateOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Date, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        obj, created = self.model.objects.update_or_create(
            img=self.img_instance, defaults=data
        )

    def get_category_data(self):
        """
        获取分类数据。
        """

        dates = self.img_instance.dates
        # 使用模型字段值构建日期对象
        # print(type(dates.year), type(dates.month), type(dates.day))
        date_obj = datetime(int(dates.year), int(dates.month), int(dates.day))
        field_list = [
            'date',
            date_obj.year,
            f'{date_obj.year:02d}-{date_obj.month:02d}',
            f'{date_obj.year}-{date_obj.month:02d}-{date_obj.day:02d}',
        ]
        return {
            'date': field_list,
        }
