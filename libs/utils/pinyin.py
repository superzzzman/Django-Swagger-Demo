# coding: utf-8

"""拼音"""

from pypinyin import pinyin, NORMAL


def str_to_pinyin(hans, style=NORMAL):
    """字符串转拼音

    :param hans: str: 汉字字符串
    :param style: int: 转换方式
    :return: str
    """
    return ''.join(sl[0] for sl in pinyin(hans, style=style))
