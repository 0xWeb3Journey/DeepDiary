import logging

import numpy as np
from insightface.app import FaceAnalysis

from deep_diary.settings import calib
from library.process.base_processor import ImageProcessor
from library.process.imagga import imagga_get, imagga_api_call
from utilities.common import trace_function


logger = logging.getLogger(__name__)
class CategoryProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)

    @trace_function
    def get(self, *args, **kwargs):
        if not self.path:
            logger.error(f"Invalid image path '{self.path}' for tag processor.")
            return None

        endpoint = 'categories/personal_photos'
        method = 'post' if self.img_type == 'path' else 'get'
        response = imagga_api_call(self.path, endpoint,
                                   method=method)
        """
        {
    "category": [
        {
            "confidence": 77.8242874145508,
            "name": {
                "en": "people portraits"
            }
        },
        {
            "confidence": 11.8529825210571,
            "name": {
                "en": "nature landscape"
            }
        },
        {
            "confidence": 4.58788299560547,
            "name": {
                "en": "food drinks"
            }
        },
        {
            "confidence": 2.78250885009766,
            "name": {
                "en": "paintings art"
            }
        },
        {
            "confidence": 1.26380443572998,
            "name": {
                "en": "pets animals"
            }
        }
    ]
}
        """
        # 检查响应并提取分类信息
        if 'result' in response and 'categories' in response['result']:
            categories = response['result']['categories']
            # 仅提取置信度大于25的分类信息
            data = [['category', cate['name']['en']] for cate in categories if cate['confidence'] > 25]
            return {'category': data}  # 返回包含分类信息的字典

        return None  # 如果响应中没有分类信息，则返回None


