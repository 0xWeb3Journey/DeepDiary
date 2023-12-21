# experience_operation.py
# force on dealing with Experience model
import logging

from django.db import transaction

from user_info.models import Experience
from user_info.operation.base_operation import BaseOperation
from utilities.common import trace_function

logger = logging.getLogger(__name__)


class ExperienceOperation(BaseOperation):

    def __init__(self, profile_instance=None):
        super().__init__(Experience, profile_instance)
        # 获取或者创建company实例， Company 和 Profile 是通过Experience 关联的多对多关系


    @transaction.atomic
    @trace_function
    def save(self, data) -> None:
        pass

    def get_pinyin(self):
        pass