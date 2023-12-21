import logging

logger = logging.getLogger(__name__)


class CeleryTaskManager:
    """
    Celery任务管理器
    """

    def __init__(self, enabled=True):
        self.enabled = enabled

    def post_process(self, img_id, f_path=None, processor_types=None, force=False, index=1, total_imgs=1):
        pass
