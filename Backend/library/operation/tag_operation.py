# img_operation.py
# force on dealing with Img model
from django.db import models
from django.db.models import Count
from taggit.models import Tag

from library.models import Img
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class TagOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Tag, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        self.img_instance.tags.add(*data)

    def clear(self, *args, **kwargs):
        self.img_instance.tags.set('')

    @staticmethod
    @trace_function
    def delete_orphan_tags():
        # The same method we defined earlier
        tags_with_counts = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).filter(num_times=0)
        tags_with_counts.delete()
