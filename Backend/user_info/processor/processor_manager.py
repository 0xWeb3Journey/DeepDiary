# from django.core.files import File
from library.process.base_processor import ImageProcessor
from library.process.exif_processor import ExifProcessor
from library.process.face_processor import FaceProcessor
from user_info.processor.profile_processor import ProfileProcessor


# from utils.mcs_storage import upload_file_pay


class ProcessorManager:
    def __init__(self, profile):
        self.profile_processor = None
        self.processors = {
            'profile': ProfileProcessor,
            # ... 其他类型 ...
        }

    def get(self, processor_type, attributes=None, *args, **kwargs):
        # 获取带有所需数据的处理器并调用其get方法
        processor = self.get_processor(processor_type, attributes)
        return processor.get(*args, **kwargs)

    def get_processor(self, processor_type, attributes=None):
        # 根据类型初始化对应的处理器

        processor_cls = self.processors.get(processor_type)
        if not processor_cls:
            raise ValueError(f"Processor type '{processor_type}' is not supported.")

        processor = processor_cls()

        return processor
