# 配置文件 celeryconfig.py

broker_url = 'redis://127.0.0.1:6379/2'
result_backend = 'redis://127.0.0.1:6379/1'


# using serializer name
accept_content = ['json', 'pickle']
task_serializer = 'pickle'
result_serializer = 'pickle'

