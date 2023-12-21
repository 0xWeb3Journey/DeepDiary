import uuid
from functools import wraps
from datetime import datetime
import pypinyin
from pypinyin import lazy_pinyin, pinyin, Style

from deep_diary.settings import cfg

start_color = "\033[92m"  # 绿色文本开始
end_color = "\033[0m"  # 重置为默认颜色
highlight_color = "\033[1;33m"  # 黄色高亮文本开始


def trace_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('-------------------------------------------------------------------------------↓👇')
        # 检查是否有参数以及第一个参数是否有__class__属性
        if args and hasattr(args[0], '__class__'):
            cls_name = args[0].__class__.__name__
            print(f"{start_color}Class: {cls_name}, Function: {func.__name__} - Started{end_color}")
        else:
            print(f"{start_color}Function: {func.__name__} - Started{end_color}")

        # ... 函数执行 ...
        # 获取开始时间
        start = datetime.now()
        result = func(*args, **kwargs)
        # 获取结束时间
        end = datetime.now()

        if args and hasattr(args[0], '__class__'):
            cls_name = args[0].__class__.__name__
            print(f"{start_color}Class: {cls_name}, Function: {func.__name__} - Ended in {end - start}sec{end_color}")
        else:
            print(f"{start_color}Function: {func.__name__} - Ended in {end - start}sec{end_color}")
        print('-------------------------------------------------------------------------------↑👆')
        return result

    return wrapper


def get_pinyin(name):
    if name is None:
        return None, None
    # full_pinyin = ''.join([item[0] for item in pinyin(name, style=Style.NORMAL)])
    full_pinyin = ''.join(lazy_pinyin(name))
    lazy_pinyin_str = ''.join(lazy_pinyin(name, style=Style.FIRST_LETTER))
    return full_pinyin, lazy_pinyin_str


def get_process_cmd(query_params):
    force = query_params.get("force", None) == '1'
    get_list_org = query_params.get("get_list", "")
    add_list_org = query_params.get("add_list", "")

    def parse_list_param(param, all_list):
        if param == 'all':
            return all_list
        return [item.strip() for item in param.split(',') if item]

    default_process_list = cfg["img"]["process_list"]
    default_add_list = cfg["img"]["add_list"]

    get_list = parse_list_param(get_list_org, default_process_list)
    add_list = parse_list_param(add_list_org, default_add_list)

    print(f'INFO:-> param force: {force}')
    print(f'INFO:-> param get_list: {get_list_org}')
    print(f'INFO:-> param add_list: {add_list_org}')
    return force, get_list, add_list


def generate_unique_name(length=20):
    return str(uuid.uuid4())[:length]  # 生成UUID并转换为40字符以内的字符串
