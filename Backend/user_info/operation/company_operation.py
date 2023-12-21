# company_operation.py
# force on dealing with Company model
from django.db import transaction
from user_info.models import Company
from user_info.operation.base_operation import BaseOperation
from utilities.common import trace_function, get_pinyin
import logging
logger = logging.getLogger(__name__)


class CompanyOperation(BaseOperation):

    def __init__(self, profile_instance=None):
        # 由于Stat是一个独立的模型，这里直接调用父类初始化方法即可
        super().__init__(Company, profile_instance)
        # 获取或者创建company实例， Company 和 Profile 是通过Experience 关联的多对多关系
        self.company_instance = self.model.Objects.get_or_create(employees=profile_instance)

    @transaction.atomic
    @trace_function
    def save(self, data) -> None:
        pass

    def get_pinyin(self):
        try:
            self.company_instance.name_PyFull, self.company_instance.name_PyInitial = get_pinyin(self.company_instance.name)
            self.company_instance.save()
        except Exception as e:
            # 处理异常（例如：日志记录）
            logger.error(f"Error while getting pinyin: {e}")
        return self.company_instance
