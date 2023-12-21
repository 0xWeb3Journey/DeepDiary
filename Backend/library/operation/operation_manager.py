# operation_manager.py
# force on manage all the operations
from django.db import transaction

from library.operation.addr_operation import AddressOperation
from library.operation.category_operation import CategoryOperation
from library.operation.color_backgound_operation import ColorBackgroundOperation
from library.operation.color_foreground_operation import ColorForegroundOperation
from library.operation.color_img_operation import ColorImgOperation
from library.operation.color_operation import ColorOperation
from library.operation.date_operation import DateOperation
from library.operation.eval_operation import EvaluateOperation
from library.operation.face_operation import FaceOperation
from library.operation.img_operation import ImgOperation
from library.operation.stat_operation import StatOperation
from library.operation.tag_operation import TagOperation
from user_info.operation.profile_operation import ProfileOperation
from utilities.common import trace_function


class OperationManager:
    def __init__(self, img_instance=None):
        self.img_instance = img_instance
        self.operation_cache = {}  # 缓存操作实例
        # 存储所有可用的操作类
        self.operations = {
            'stat': StatOperation,
            'face': FaceOperation,
            'img': ImgOperation,
            'addr': AddressOperation,
            'eval': EvaluateOperation,
            'date': DateOperation,
            'tag': TagOperation,
            'color_background': ColorBackgroundOperation,
            'color_foreground': ColorForegroundOperation,
            'color_img': ColorImgOperation,
            'color_info': ColorOperation,
            'category': CategoryOperation,
            'clip_classification': CategoryOperation,
            'caption': ImgOperation,
            'feature': ImgOperation,
        }

    def get_operation(self, model_name):
        if model_name not in self.operation_cache:
            operation_cls = self.operations.get(model_name)
            if not operation_cls:
                raise ValueError(f"Operation for model '{model_name}' is not available.")
            self.operation_cache[model_name] = operation_cls(self.img_instance)
        return self.operation_cache[model_name]

    def execute(self, model_name, method_name, *args, **kwargs):
        """
        执行指定模型的操作方法。
        """
        operation = self.get_operation(model_name)
        method = getattr(operation, method_name, None)
        if not method:
            raise AttributeError(f"The method '{method_name}' is not defined in '{model_name}' operation.")
        return method(*args, **kwargs)

    def get_category_data(self, process_type):
        # 根据 process_type 获取相应类型的分类数据
        if process_type not in self.operations:
            raise ValueError(f"Unsupported process type: {process_type}")

        operation = self.get_operation(process_type)
        if hasattr(operation, 'get_category_data'):
            return operation.get_category_data()
        else:
            raise NotImplementedError(f"'get_data' method not implemented in {process_type} operation.")

    def add_to_category(self, category_data):
        # 将数据添加到分类中
        for key, value in category_data.items():  # 这里的value 是个列表
            if value:  # 检查数据是否有效
                # field_list = self.format_category_field(key, value)
                self.execute('category', 'save', value)

    @trace_function
    def category_get_and_add(self, process_type):
        # 使用字典推导式处理列表
        data = {k: v for item in process_type for k, v in self.get_category_data(item).items()} if isinstance(
            process_type, list) else self.get_category_data(process_type)

        if not isinstance(process_type, (list, str)):
            raise ValueError(f"Invalid data type for process_type: {type(process_type)}")

        print(f'INFO: the data is {data}')
        self.add_to_category(data)

    def format_category_field(self, key, value):
        # 根据key和value格式化成category的字段列表
        # 这里需要根据实际情况来定制字段格式化逻辑
        field_list = [key]
        field_list.extend(value)  # 假设value是一个列表
        return field_list

    # @trace_function
    @transaction.atomic
    def save_data(self, data: dict):
        # 通用保存方法
        for key, operation in self.operations.items():
            if data.get(key):
                self.execute(key, 'save', data[key])

    # @trace_function
    @transaction.atomic
    def delete(self, data: dict):
        # 通用保存方法
        for key, operation in self.operations.items():
            if data.get(key):
                self.execute(key, 'delete', data[key])

    # @trace_function
    @transaction.atomic
    def clear_existed_data(self, operations_to_clear):
        # 通用清除特定操作的方法
        valid_operations_to_clear = ['tag', 'face', 'color_img', 'color_background', 'color_foreground']  # 'category'
        # color 操作包含 color_img, color_background, color_foreground等模型，所以这里需要特殊处理
        operations_to_clear = ['color_info', 'color_img', 'color_background', 'color_foreground'] if operations_to_clear == 'color' else operations_to_clear

        if isinstance(operations_to_clear, list):
            for operation in operations_to_clear:
                if operation in valid_operations_to_clear:
                    self.execute(operation, 'clear')
        elif isinstance(operations_to_clear, str):
            if operations_to_clear in valid_operations_to_clear:
                self.execute(operations_to_clear, 'clear')
        else:
            raise ValueError(f"Invalid data type for clear_specific_operations: {type(operations_to_clear)}")

        # 可以在这里添加后续的逻辑，例如打印清除操作完成的消息等

    # @trace_function
    @transaction.atomic
    def update_data(self, data_type, data: dict):
        # 通用保存方法
        for key, operation in self.operations.items():
            if key != 'stat' and data.get(key):
                self.execute(key, 'update', data[key])
        self.execute('stat', 'update_stats_flag', data_type)
