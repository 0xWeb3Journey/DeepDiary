# img_operation.py
# force on dealing with Img model
from django.db import models

from library.models import Img, Address
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


class AddressOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Address, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        obj, created = self.model.objects.update_or_create(
            img=self.img_instance, defaults=data
        )

    def get_category_data(self):
        """
        获取分类数据。
        """
        addr = self.img_instance.address
        field_list = [
            'location',
            addr.country if addr.country and addr.country != '[]' else 'No GPS',
            addr.province if addr.province and addr.province != '[]' else 'No GPS',
            addr.city if addr.city and addr.city != '[]' else 'No GPS',
            addr.district if addr.district and addr.district != '[]' else 'No GPS',
        ]
        data = {
            'addr': field_list,
        }
        return data
