import pypinyin
from pypinyin import lazy_pinyin, pinyin, Style


def get_pinyin(name):
    # full_pinyin = ''.join([item[0] for item in pinyin(name, style=Style.NORMAL)])
    full_pinyin = ''.join(lazy_pinyin(name))
    lazy_pinyin_str = ''.join(lazy_pinyin(name, style=Style.FIRST_LETTER))
    return full_pinyin, lazy_pinyin_str


# 示例
# chinese_name = "葛维冬"
# full_pinyin, lazy_pinyin_str = get_pinyin(chinese_name)
# print("Full Pinyin:", full_pinyin)  # 输出：geweidong
# print("Lazy Pinyin:", lazy_pinyin_str)  # 输出：gwd
