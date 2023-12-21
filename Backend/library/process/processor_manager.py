# from django.core.files import File
from library.process.base_processor import ImageProcessor
from library.process.caption_processor import CaptionProcessor
from library.process.category_processor import CategoryProcessor
from library.process.clip_calssification_processor import ClipClassificationProcessor
from library.process.color_processor import ColorProcessor
from library.process.exif_processor import ExifProcessor
from library.process.face_processor import FaceProcessor
from library.process.feature_processor import FeatureProcessor
from library.process.mcs_processor import McsProcessor
from library.process.tag_processor import TagProcessor


# from utils.mcs_storage import upload_file_pay


class ProcessorManager:
    def __init__(self, img):
        self.img_processor = ImageProcessor(img)
        # 如果不是有效类型，则直接返回
        if not self.img_processor.img_type:
            return
        self.img_processor.read()
        self.processors = {
            'exif': ExifProcessor,
            'face': FaceProcessor,
            'tag': TagProcessor,
            'color': ColorProcessor,
            'category': CategoryProcessor,
            'feature': FeatureProcessor,
            'caption': CaptionProcessor,
            'mcs': McsProcessor,
            'clip_classification': ClipClassificationProcessor,
            # ... 其他类型 ...
        }

    def get(self, processor_type, attributes=None, *args, **kwargs):
        # 获取带有所需数据的处理器并调用其get方法
        processor = self.get_processor(processor_type, attributes)
        data = processor.get(*args, **kwargs)
        if not data:
            print(f"No data to process for {processor_type}.")
        # else:
        #     print(f'Info: process result is {data}')

        return data

    def get_processor(self, processor_type, attributes=None):
        # 根据类型初始化对应的处理器

        processor_cls = self.processors.get(processor_type)
        if not processor_cls:
            raise ValueError(f"Processor type '{processor_type}' is not supported.")

        processor = processor_cls(self.img_processor.img)
        if attributes is None:
            attributes = [attr for attr in dir(self.img_processor) if
                          not attr.startswith("__") and not callable(getattr(self.img_processor, attr))]
        # print(f'INFO: get_processor----->attributes is {attributes} ')

        # 根据属性列表选择性地传递图像数据给处理器
        for attribute in attributes:
            if hasattr(self.img_processor, attribute):
                setattr(processor, attribute, getattr(self.img_processor, attribute))

        return processor
