import logging

import numpy as np
from insightface.app import FaceAnalysis

from deep_diary.settings import calib
from library.process.base_processor import ImageProcessor
from library.process.imagga import imagga_get, imagga_api_call
from utilities.common import trace_function


logger = logging.getLogger(__name__)


class ColorProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)

    @trace_function
    def get(self):
        if not self.path:
            logger.error(f"Invalid image path '{self.path}' for tag processor.")
            return None

        method = 'post' if self.img_type == 'path' else 'get'
        response = imagga_api_call(self.path, 'colors',
                                   method=method)

        # 检查响应状态
        if response.get('status', {}).get('type') != 'success':
            print("Failed to retrieve color data")
            return {}

        color_data = response.get('result', {}).get('colors', {})
        keys_to_extract = ["color_percent_threshold", "color_variance", "object_percentage"]
        return {
            'color_info': {key: color_data[key] for key in keys_to_extract},
            'color_background': color_data.get('background_colors', []),
            'color_foreground': color_data.get('foreground_colors', []),
            'color_img': color_data.get('image_colors', [])
        }