# Resource_operation.py
# force on dealing with Resource model
import logging

from django.db import transaction

from user_info.models import Resource
from user_info.operation.base_operation import BaseOperation
from utilities.common import trace_function

logger = logging.getLogger(__name__)


class ResourceOperation(BaseOperation):

    def __init__(self, profile_instance=None):
        super().__init__(Resource, profile_instance)


    @transaction.atomic
    @trace_function
    def save(self, data) -> None:
        pass

    def get_pinyin(self):
        pass