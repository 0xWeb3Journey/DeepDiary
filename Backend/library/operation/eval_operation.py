# img_operation.py
# force on dealing with Img model
from django.db import models

from library.models import Img, Evaluate
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class EvaluateOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Evaluate, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        obj, created = self.model.objects.update_or_create(
            img=self.img_instance, defaults=data
        )
