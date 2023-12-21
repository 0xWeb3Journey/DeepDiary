# img_operation.py
# force on dealing with Img model

import clip
import numpy as np
import torch

from library.models import Img, Category
from library.operation.base_operation import BaseOperation
from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class CategoryOperation(BaseOperation):
    def __init__(self, img_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Category, img_instance)

    @trace_function
    def save(self, data, *args, **kwargs):
        # 判断data是否为二维列表
        if all(isinstance(item, list) for item in data):
            # data是二维列表，遍历每个子列表
            for sublist in data:
                self.__add_levels_to_category__(instance=self.img_instance, field_list=sublist)
        elif isinstance(data, list):
            # data是一维列表，直接调用函数
            self.__add_levels_to_category__(instance=self.img_instance, field_list=data)
        else:
            # data不是列表，抛出异常
            raise ValueError("Invalid data type for 'data'. Expected a list or a list of lists.")

    # def __add_levels_to_category__(self, instance=None, field_list=None, force=True):
    #
    #     """
    #     purpose: add the levels to the category， which class is class Category(MPTTModel):
    #     :param instance: the instance of the image
    #     :param field_list: the list of the field, the first item is the level 0, then the level 1, level 2, level 3
    #     :return: category instance
    #     """
    #     levels = len(field_list)
    #     if not levels:
    #         print(f'INFO: there is no field_list')
    #         return
    #
    #     parent_obj = None
    #
    #     # 2. check the root category is existed or not, if not, create it
    #     # parent_obj, created = Category.objects.get_or_create(name=field_list[0], defaults=creation_params)
    #     # 3. loop the field_list
    #     print(f'INFO: the field_list is {field_list}, will be added to the category')
    #     for (idx, field) in enumerate(field_list):
    #         # if idx == 0:  # skip the first item
    #         #     continue
    #         creation_params = {
    #             'level': idx,
    #             'is_leaf': True if idx == levels - 1 else False,
    #             'is_root': True if idx == 0 else False,
    #             'owner': instance.user,
    #             'avatar': instance.src,
    #             'description': f'this is {field} category',
    #             'parent': None if idx == 0 else parent_obj,
    #         }
    #         get_params = {
    #             'parent': None if idx == 0 else parent_obj,
    #             'name': field,
    #         }
    #         category_obj, created = Category.objects.get_or_create(**get_params, defaults=creation_params)
    #         # category_obj, created = Category.objects.get_or_create(name=field, defaults=creation_params)
    #         # add the instance to the category
    #         category_obj.imgs.add(instance)
    #         parent_obj = category_obj
    #     return parent_obj

    def __add_levels_to_category__(self, instance=None, field_list=None):
        if not field_list:
            print(f'INFO: No field_list provided for category creation')
            return None

        parent_obj = None
        print(f'INFO: Adding categories {field_list} to the category tree')

        for idx, field in enumerate(field_list):
            creation_params = {
                'level': idx,
                'is_leaf': idx == len(field_list) - 1,
                'is_root': idx == 0,
                'owner': instance.user,
                'avatar': instance.src,
                'description': f'This is {field} category',
                'parent': parent_obj,
            }
            category_obj, created = Category.objects.get_or_create(
                name=field,
                defaults=creation_params,
                parent=parent_obj
            )
            category_obj.imgs.add(instance)
            parent_obj = category_obj

        return parent_obj

    def clear(self):
        """
        清除已存在的人脸数据。
        """
        objs = (self.model.objects.filter(imgs=self.img_instance, is_root=False))
        # 打印objs的长度
        print(f"objs length is {len(objs)}")
        objs.delete()
