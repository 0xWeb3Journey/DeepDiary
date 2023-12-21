import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deep_diary.settings')
django.setup()
from deep_diary.settings import cfg

from utilities.mcs_storage import upload_file_pay


# from django.test import TestCase
from library.models import Img
from library.tasks import CeleryTaskManager, logger_test
from library.task_manager import LibraryTaskManager
from user_info.task_manager import UserInfoTaskManager

# class ImgProcessTest(TestCase):
#     def setUp(self):
#         # 创建测试用户和图片
#
#         self.img_instance = Img.objects.get(id=1799)
#
#     def test_read_img_instance(self):
#         # 测试读取Img实例
#         img_processor = ImgProces(instance=self.img_instance)
#         result = img_processor.read(self.img_instance)
#
#         self.assertIsNotNone(result[0], "img_exiv2 should not be None")
#         self.assertIsNotNone(result[1], "img_pil should not be None")
#         self.assertIsNotNone(result[2], "img_cv2 should not be None")
#         self.assertIsNotNone(result[3], "base64 should not be None")
#
#     # 以下是其他测试用例，用于测试本地路径、网络图片和二进制文件流等
#     # ...


# 运行测试

#
if __name__ == '__main__':
    # ImgProcessTest()

    # 以下是测试用例，用于测试本地路径、网络图片和二进制文件流等
    # img_instance = Img.objects.all().first()
    img_instance = Img.objects.get(id=622)
    path = r'd:\BlueDoc\DiaryWin\source\img\已上传\IMG_20200815_151915.jpg'
    url = 'https://deep-diary.oss-accelerate.aliyuncs.com/media/blue/img/IMG_20200815_151915.jpg'
    # 根据上面的path图片，帮我构建如下3个类的实例，作为测试用例

    user_info_task_manager = UserInfoTaskManager()
    library_task_manager = LibraryTaskManager(path, img_instance, user_info_task_manager=user_info_task_manager)
    # library_task_manager.operation_manager.category_get_and_add('color_background')
    # library_task_manager.operation_manager.category_get_and_add('color_foreground')
    # library_task_manager.operation_manager.category_get_and_add('color_img')
    # library_task_manager.operation_manager.category_get_and_add(['img', 'face'])
    # library_task_manager.operation_manager.clear_existed_data(['tag'])
    # library_task_manager.operation_manager.clear_existed_data('color')
    # library_task_manager.process_and_save('exif', force=True)
    # library_task_manager.process_and_save('category', force=True)

    # tasks = ['exif', 'face', 'tag', 'color', 'category', 'clip_classification', 'feature', 'caption']
    tasks = ['category']
    CeleryTaskManager(enabled=False).post_process(img_instance.id, f_path=img_instance, processor_types=tasks, force=True)
    # CeleryTaskManager(enabled=False).category_get_and_add(img_instance.id, processor_types=['color_img', 'img', 'addr'], force=True)

    print('done')
