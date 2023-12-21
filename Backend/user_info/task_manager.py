# 管理app内相关操作及celery任务的执行。
import os

from user_info.models import Profile
from user_info.operation.operation_manager import OperationManager
from user_info.processor.processor_manager import ProcessorManager
from utilities.common import trace_function


class UserInfoTaskManager:
    def __init__(self, profile=None, **kwargs):
        # 图片路径: path, url, Img instance
        self.profile = self.get_profile_instance(profile)

        # 外部app Task管理器
        self.library_task_manager = kwargs.get('library_task_manager', None)
        # 内部app Task管理器
        self.processor_manager = ProcessorManager(profile)
        self.operation_manager = OperationManager(profile)

    def get_profile_instance(self, profile_instance):
        # 确保img是一个Img实例或者获取Img实例
        instance = None
        if isinstance(profile_instance, Profile):
            instance = profile_instance
        return instance

    @trace_function
    def process_and_save(self, processor_type, force=False, *args, **kwargs):
        # 判断processor_type是否有效
        if processor_type not in self.tasks:
            print(f"Invalid processor type '{processor_type}'.")
            return
        # 判断是否需要处理
        if not self.operation_manager.get_operation('stat').is_process_needed(processor_type, force=force):
            print("No valid image instance available for processing.")
            return
        # 获取数据
        data = self.processor_manager.get(processor_type)
        if not data:
            print(f"No data to process for {processor_type}.")
            return

        # 对数据进行后处理（如需要）
        processed_data = self.data_post_process(processor_type, data)
        self.operation_manager.save_data(processor_type, processed_data)

    def data_post_process(self, processor_type, data):
        if processor_type == 'exif':
            pass
        elif processor_type == 'face':
            pass

        # 其他处理类型的后处理逻辑
        # TODO: 添加其他类型的数据处理
        return data
