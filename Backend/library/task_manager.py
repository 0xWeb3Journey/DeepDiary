# task_manager.py
# 管理app内相关操作及celery任务的执行。
import json
import os

from library.models import Img, Stat
from library.operation.operation_manager import OperationManager
from library.process.processor_manager import ProcessorManager

from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay

class LibraryTaskManager:
    def __init__(self, img=None, img_instance=None, **kwargs):
        self.img = img
        self.instance = img_instance if isinstance(img_instance, Img) else self.get_image_instance(img)
        self.user_info_task_manager = kwargs.get('user_info_task_manager', None)
        self.processor_manager = ProcessorManager(img)
        self.operation_manager = OperationManager(img_instance)

    def get_image_instance(self, img):
        if isinstance(img, str):
            try:
                return Img.objects.get(name=os.path.basename(img))
            except Img.DoesNotExist:
                print(f"Img instance with name '{os.path.basename(img)}' does not exist.")
        return None

    # @trace_function
    def process_and_save(self, processor_type, force=False, *args, **kwargs):

        # 判断是否需要处理
        if not self.operation_manager.get_operation('stat').is_process_needed(processor_type, force=force):
            return
        # 获取数据
        data = self.processor_manager.get(processor_type)
        if not data:
            return
        # 对数据进行后处理（如需要）
        processed_data = self.data_post_process(processor_type, data)

        # 清空已有数据（如需要）, 主要针对一些外键关联的数据，如tag、face、color、category等
        if force:
            self.operation_manager.clear_existed_data(processor_type)
        # 保存数据
        self.operation_manager.save_data(processed_data)

    @trace_function
    def process_and_update(self, processor_type, force=False, *args, **kwargs):
        # 判断是否需要处理
        if not self.operation_manager.get_operation('stat').is_process_needed(processor_type, force=force):
            return
        # 获取数据
        data = self.processor_manager.get(processor_type)
        if not self.processor_manager.get(processor_type):
            return

        # 对数据进行后处理（如需要）
        processed_data = self.data_post_process(processor_type, data)

        # TODO: 清空已有数据（如需要）

        # 更新数据
        self.operation_manager.update_data(processor_type, processed_data)

    def data_post_process(self, processor_type, data):
        """
        对数据进行后处理。主要处理整合外部app的数据，还有状态位的设置。
        """
        # 初始化统一的数据结构
        processed_data = {'stat': {processor_type: True, 'is_has_exif': True}}

        if processor_type == 'exif':
            processed_data['stat']['is_has_exif'] = bool(data)
            processed_data.update(data)
        elif processor_type == 'face':
            face_data = [dt['fc'] for dt in data['face']]
            profiles = self.user_info_task_manager.operation_manager.get_operation('profile').get_profiles(face_data)
            data['profiles'] = profiles
            processed_data['face'] = data
        elif processor_type == 'tag':
            # TODO: 添加tag数据的处理逻辑
            pass
        else:
            # 其他处理类型的后处理逻辑
            processed_data = {**processed_data, **data}

        return processed_data
