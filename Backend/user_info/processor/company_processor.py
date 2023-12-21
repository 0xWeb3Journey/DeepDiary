import numpy as np
from insightface.app import FaceAnalysis

from deep_diary.settings import calib
from library.process.base_processor import ImageProcessor
from utilities.common import trace_function


# from django.core.files import File
# from utils.mcs_storage import upload_file_pay


class FaceProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, profile_instance=None):
        super().__init__(profile_instance)
        pass

    @trace_function
    def get(self, *args, **kwargs):
        pass