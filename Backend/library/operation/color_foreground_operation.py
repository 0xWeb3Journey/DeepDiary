# img_operation.py
# force on dealing with Img model
from django.db import models
from django.db.models import Count
from taggit.models import Tag

from library.models import Img, ImgMcs, ColorBackground, ColorForeground
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class ColorForegroundOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(ColorForeground, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        self.clear()
        if isinstance(data, list):
            objs = []
            for item in data:
                obj = self.model.objects.create(
                    img=self.img_instance, **item
                )
                objs.append(obj)
            return objs
        else:
            obj = self.model.objects.create(
                img=self.img_instance, **data
            )
            return obj

    def get_category_data(self):
        data = {}
        color_back = self.img_instance.cbacks.all()
        for idx, color in enumerate(color_back):
            field_list = [
                'color_fore',
                # color_palette[color.closest_palette_color_parent]
                color.closest_palette_color_parent
            ]
            data.update({
                f'color_fore_{idx}': field_list,
            })
        return data
