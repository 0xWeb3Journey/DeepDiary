import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

# 项目名称
project_name = 'deep_diary'
# Django项目的设置文件
project_settings = '%s.settings' % project_name

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

# 创建Celery应用
app = Celery(project_name)
# 使用Django的配置文件进行配置
app.config_from_object('deep_diary.celeryconfig')

# 设置时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 任务的定时配置
app.conf.beat_schedule = {
    # 每5分钟检查所有图片信息的任务
    'check_all_img_info': {
        'task': 'library.task.check_all_img_info',
        'schedule': timedelta(seconds=5*60),
        'args': (None, None, False,),  # None表示处理所有图片
    },
    # 测试任务，每5秒执行一次
    'test': {
        'task': 'library.task.test',
        'schedule': timedelta(seconds=5),
        'args': ('deep-diary is running',),
    },
    # 每天早上8点和晚上8点执行的任务
    'scheduled_task': {
        'task': 'library.task.some_task',  # 修改为您的具体任务名称
        'schedule': crontab(hour=[8, 20], minute=0),
        'args': (),  # 按需要添加适当的参数
    }
}
