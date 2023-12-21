import logging

from user_info.operation.assert_operation import AssertOperation
from user_info.operation.company_operation import CompanyOperation
from user_info.operation.demand_operation import DemandOperation
from user_info.operation.experience_operation import ExperienceOperation
from user_info.operation.profile_operation import ProfileOperation
from user_info.operation.resource_operation import ResourceOperation

logger = logging.getLogger(__name__)


class OperationManager:
    def __init__(self, profile_instance=None):
        self.profile_instance = profile_instance
        # 存储所有可用的操作类
        self.operations = {
            'profile': ProfileOperation,
            'company': CompanyOperation,
            'assert': AssertOperation,
            'experience': ExperienceOperation,
            'resource': ResourceOperation,
            'demand': DemandOperation,
            # 'stat': StatOperation,
            # ... 其他操作类 ...
        }

    def get_operation(self, model_name):
        """
        根据模型名获取相应的操作类。
        """
        operation_cls = self.operations.get(model_name)
        if not operation_cls:
            raise ValueError(f"Operation for model '{model_name}' is not available.")
        operation = operation_cls()
        operation.profile_instance = self.profile_instance
        return operation

    def execute(self, model_name, method_name, *args, **kwargs):
        """
        执行指定模型的操作方法。
        """
        operation = self.get_operation(model_name)
        method = getattr(operation, method_name, None)
        if not method:
            raise AttributeError(f"The method '{method_name}' is not defined in '{model_name}' operation.")
        return method(*args, **kwargs)

    def save_data(self, data_type, data: dict):
        # 通用保存方法
        for key, operation in self.operations.items():
            if key != 'stat' and data.get(key):
                self.execute(key, 'save', data[key])
        self.execute('stat', 'update_stats_flag', data_type)

    def face_rename(self, face_instance, new_name=None):
        """
        重命名人脸文件
        """
        self.profile_instance, face_instance = self.get_operation('profile').face_rename(face_instance,
                                                                                         new_name=new_name)
        self.get_operation('assert').update_asserts()

        return self.profile_instance, face_instance
