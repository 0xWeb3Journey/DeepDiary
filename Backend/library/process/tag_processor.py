import logging

from library.process.base_processor import ImageProcessor
from library.process.imagga import imagga_get, imagga_post, imagga_api_call
from utilities.common import trace_function

logger = logging.getLogger(__name__)


class TagProcessor(ImageProcessor):
    # ... 其他方法 ...
    # def __init__(self, image_processor):

    def __init__(self, img=None):
        super().__init__(img)

    @trace_function
    def get(self, *args, **kwargs):
        tags = []

        if not self.path:
            logger.error(f"Invalid image path '{self.path}' for tag processor.")
            return None

        method = 'post' if self.img_type == 'path' else 'get'
        response = imagga_api_call(self.path, 'tags',
                                   query={'verbose': False, 'language': 'en', 'threshold': 25},
                                   method=method)

        if 'result' in response:
            tags = [tag['tag']['en'] for tag in response['result']['tags']]
        data = {
            'tag': tags,
        }
        return data
