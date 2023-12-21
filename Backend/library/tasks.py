# tasks.py
# 用于管理所有Celery任务
import base64

# tasks.py

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import os
from celery import shared_task
from library.models import Img
from library.task_manager import LibraryTaskManager
from user_info.task_manager import UserInfoTaskManager
from utilities.common import trace_function
import logging

logger = logging.getLogger(__name__)


def logger_test():
    # Instead of print, use logger
    logger.debug("This is a debug message")
    logger.info("This is an informational message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


def get_img_instance(img_id):
    try:
        return Img.objects.get(pk=img_id)
    except Img.DoesNotExist:
        print(f'Image with ID {img_id} does not exist.')
        return None


def get_imgs_to_process(processor_types, force):
    query_filter = {f'stats__is_get_{pt}': False for pt in processor_types}
    return Img.objects.all() if force else Img.objects.filter(**query_filter)


@shared_task
@trace_function
def upload_file_task(temp_file_path, file_name, img_id):
    img_ins = get_img_instance(img_id)
    if not img_ins:
        logger.error(f'Image with ID {img_id} does not exist.')
        return

    try:
        # 使用文件路径创建文件对象
        with open(temp_file_path, 'rb') as f:
            django_file = File(f, name=file_name)
            img_ins.src = django_file
            img_ins.save(update_fields=['src'])  # ['src', *kwargs.keys()]

    except Exception as e:
        # 处理任何可能发生的异常
        print(f"上传文件任务失败: {str(e)}")
        # 这里可以记录日志或执行其他错误处理逻辑
        return {"status": "error", "message": str(e)}
    #
    tasks = ['exif', 'face', 'tag', 'color', 'category', 'clip_classification', 'feature', 'caption']
    post_process(img_id, processor_types=tasks, force=True)  # f_path=temp_file_path,
    # post_process.delay(img_id, f_path=temp_file_path, processor_types=tasks, force=True)
    # 可选：处理完成后删除临时文件
    # os.remove(temp_file_path)
    # 返回成功消息
    return {"status": "success", "message": "文件上传成功"}


@shared_task
@trace_function
def post_process(img_id, f_path=None, processor_types=None, force=False, index=1, total_imgs=1):
    """
    图片后处理任务
    """
    img_ins = get_img_instance(img_id)
    if not img_ins:
        logger.error(f'Image with ID {img_id} does not exist.')
        return

    img = f_path if f_path else img_ins
    user_info_task_manager = UserInfoTaskManager()
    library_task_manager = LibraryTaskManager(img=img, img_instance=img_ins,
                                              user_info_task_manager=user_info_task_manager)

    for processor_type in processor_types or ['exif']:
        logger.info(
            f'INFO: Processing image {index}/{total_imgs} (ID: {img_ins.id}, processor_type: {processor_type}).')
        library_task_manager.process_and_save(processor_type, force=force)

    completion_percentage = (index / total_imgs) * 100
    logger.info(
        f'INFO: Image ID {img_ins.id} processing completed. {completion_percentage:.2f}% of total images processed.')


@shared_task
@trace_function
def process_all(processor_types=None, force=False):
    """
    处理所有图片
    """
    processor_types = processor_types or ['exif']

    imgs = get_imgs_to_process(processor_types, force)
    total_imgs = imgs.count()
    logger.info(f'INFO: Total {total_imgs} images to process.')

    for index, img in enumerate(imgs, start=1):
        post_process.delay(img.id, f_path=img, processor_types=processor_types, force=force, index=index,
                           total_imgs=total_imgs)


@shared_task
@trace_function
def category_get_and_add(img_id, processor_types=None, force=False, index=1, total_imgs=1):
    """
    为图片添加分类
    """
    img_ins = get_img_instance(img_id)
    if not img_ins:
        logger.error(f'Image with ID {img_id} does not exist.')
        return
    library_task_manager = LibraryTaskManager(img=img_ins, img_instance=img_ins)
    library_task_manager.operation_manager.category_get_and_add(processor_types)
    completion_percentage = (index / total_imgs) * 100
    logger.info(
        f'INFO: Image ID {img_ins.id} processing completed. {completion_percentage:.2f}% of total images processed.')


@shared_task
@trace_function
def category_get_and_add_all(processor_types=None, force=False):
    """
    为所有图片添加分类
    """
    processor_types = processor_types or ['img']

    imgs = get_imgs_to_process(processor_types, force)
    total_imgs = imgs.count()
    logger.info(f'INFO: Total {total_imgs} images to process.')

    for index, img in enumerate(imgs, start=1):
        category_get_and_add.delay(img.id, processor_types=processor_types, force=force, index=index,
                                   total_imgs=total_imgs)


class CeleryTaskManager:
    """
    Celery任务管理器
    """

    def __init__(self, enabled=True):
        self.enabled = enabled

    def post_process(self, img_id, f_path=None, processor_types=None, force=False, index=1, total_imgs=1):
        task_function = post_process.delay if self.enabled else post_process
        task_function(img_id, f_path=f_path, processor_types=processor_types, force=force, index=index,
                      total_imgs=total_imgs)

    def process_all(self, processor_types=None, force=False):
        task_function = process_all.delay if self.enabled else process_all
        task_function(processor_types=processor_types, force=force)

    def category_get_and_add(self, img_id, processor_types=None, force=False, index=1, total_imgs=1):
        task_function = category_get_and_add.delay if self.enabled else category_get_and_add
        task_function(img_id, processor_types=processor_types, force=force, index=index, total_imgs=total_imgs)

    def category_get_and_add_all(self, processor_types=None, force=False):
        task_function = category_get_and_add_all.delay if self.enabled else category_get_and_add_all
        task_function(processor_types=processor_types, force=force)

    def upload_file_task(self, temp_file_path, file_name, img_id):
        task_function = upload_file_task.delay if self.enabled else upload_file_task
        task_function(temp_file_path, file_name, img_id)
