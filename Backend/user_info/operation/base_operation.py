from django.db import models
from django.db.models import QuerySet


class BaseOperation:
    def __init__(self, model, profile_instance=None):
        self.model = model
        self.profile_instance = profile_instance

    def check_data_validity(self, data) -> bool:
        """
        检查数据是否有效, 如果全为空，则返回False。否则返回True。
        """
        if isinstance(data, dict):
            return any(value is not None for value in data.values())
        elif isinstance(data, list):
            return bool(data)
        else:
            return False

    def save(self, instance, data) -> None:
        """
        保存数据方法。子类应该根据具体的数据类型实现该方法。
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def create(self, data) -> models.Model:
        """
        创建模型实例。
        """
        if not self.check_data_validity(data):
            raise ValueError("Invalid data provided for creation.")
        instance = self.model.objects.create(**data)
        return instance

    def update(self, instance, data) -> models.Model:
        """
        更新模型实例。
        """
        if not self.check_data_validity(data):
            raise ValueError("Invalid data provided for update.")
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, instance) -> None:
        """
        删除模型实例。
        """
        instance.delete()

    def get_queryset(self, **filters) -> QuerySet:
        """
        根据给定的筛选条件获取查询集。
        """
        queryset = self.model.objects.filter(**filters)
        return queryset
