# img_operation.py
# force on dealing with Img model
from django.db import models
from django.db.models import Count
from taggit.models import Tag

from library.models import Img, ImgMcs
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class McsOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(ImgMcs, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        pass
