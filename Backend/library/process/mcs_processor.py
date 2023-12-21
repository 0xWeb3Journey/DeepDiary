import numpy as np
from insightface.app import FaceAnalysis

from deep_diary.settings import calib, cfg
from library.process.base_processor import ImageProcessor
from utilities.common import trace_function
from utilities.mcs_storage import upload_file_pay


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class McsProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)

    @trace_function
    def get(self, *args, **kwargs):
        mcs_data = upload_file_pay(cfg['wallet_info'], self.img.src.url)
        data = {
            'mcs': mcs_data
        }
        return data
