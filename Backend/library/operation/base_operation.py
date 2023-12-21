from django.db import models
from django.db.models import QuerySet

from utilities.common import trace_function


class BaseOperation:
    def __init__(self, model, img_instance=None):
        self.model = model
        self.img_instance = img_instance
        if not self.img_instance:
            raise ValueError("Image instance is not provided.")

    def check_data_validity(self, data) -> bool:
        """
        检查数据是否有效, 如果全为空，则返回False。否则返回True。
        """
        if isinstance(data, list):
            return bool(data)
        elif isinstance(data, dict):
            return bool(data)
        else:
            return False

    @trace_function
    def save(self, data, *args, **kwargs):
        """
        保存数据方法。子类应该根据具体的数据类型实现该方法。
        如果data是字典，则使用update_or_create来更新或创建单个实例。
        如果data是列表，则循环通过update_or_create来更新或创建多个实例。
        """
        print("---->BaseOperation save method is called.")

        # 判断data是否是列表
        if isinstance(data, list):
            objs = []
            for item in data:
                obj, created = self.model.objects.update_or_create(
                    img=self.img_instance, defaults=item
                )
                objs.append(obj)
            return objs
        else:  # 如果data是字典
            obj, created = self.model.objects.update_or_create(
                img=self.img_instance, defaults=data
            )
            return obj

    def create(self, data) -> models.Model:
        """
        创建模型实例。
        """
        if not self.check_data_validity(data):
            raise ValueError("Invalid data provided for creation.")
        instance = self.model.objects.create(**data)
        return instance

    @trace_function
    def update(self, data) -> models.Model:
        """
        更新模型实例。
        """
        print("---->BaseOperation update method is called.")
        if not self.check_data_validity(data):
            raise ValueError("Invalid data provided for update.")
        for field, value in data.items():
            setattr(self.img_instance, field, value)
        self.img_instance.save()
        return self.img_instance

    def delete(self, instance) -> None:
        """
        删除模型实例。
        """
        self.img_instance.delete()

    def get_queryset(self, **filters) -> QuerySet:
        """
        根据给定的筛选条件获取查询集。
        """
        queryset = self.model.objects.filter(**filters)
        return queryset

    def clear(self):
        """
        清除已存在的数据。
        """
        self.model.objects.filter(img=self.img_instance).delete()

    def get_category_data(self):
        """
        获取分类数据。
        """
        raise NotImplementedError(f"'get_category_data' method not implemented in {self.__class__.__name__}.")
