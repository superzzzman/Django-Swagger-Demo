# -*-coding:utf-8-*-

"""自定义校验方法, 异常在这里raise"""

import re
from .exception import InvalidParamType, MissingParameters, InvalidParamRange, \
    InvalidBlankParam, InvalidFile, MissingFileName, UnsupportedFileType, ParamRegexpMatchFailed
from django.core.files.uploadedfile import UploadedFile
from decimal import Decimal
from libs.utils.common import PDecimal
from collections import Iterator
from libs.utils.copy import SpecDeepcopy


class Parameters(dict):
    """
    功能说明：自定义参数，增加参数校验
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-09-04        new
    ld        2021-05-06        修改update函数
    ld        2021-05-07        新增自定义异常
    --------------------------------
    """

    def __init__(self, dic=None, **kwargs):
        if dic is not None:
            self.update(dic)
        if kwargs:
            self.update(kwargs)

    def get(self, key, default=None, must=False, add_ex_error=True, func=None, func_bak=False, lt=None,
            gt=None, lte=None, gte=None, equal=None, non_equal=None, non_contains=(), contains=(),
            decimal_length=2, round_or_raise=False, length=None, length_equal=None, length_range=None,
            check_blank=False, blank_str=None, replace_or_raise=False, replace_str='', left_blank=False,
            right_blank=False, file_check=False, file_suffix=(), key_alias=None, regexp_str=None, regexp_str_list=None,
            regexp_message=None, without_check=False, message=None, save=False, exc=None, **kwargs):
        """重写get方法，支持校验是否必传
        :param key: str: 关键字
        :param default: any: 默认值
        :param must: bool: 是否必传
        :param add_ex_error: bool: 是否在异常中添加附加信息
        :param func: func: 转换函数
        :param func_bak: bool: 是否返回转换后的值
        :param lt: any: 小于
        :param gt: any: 大于
        :param lte: any: 小于等于
        :param gte: any: 大于等于
        :param equal: any: 等于比较
        :param non_equal: any: 不等于比较
        :param non_contains: seq: not in 比较
        :param contains: seq: in比较
        :param decimal_length: int: 小数部分长度上限
        :param round_or_raise: bool: 四舍六入五成双（True）, 异常（False）
        :param length: int: 长度上限（字符串，列表，元祖）
        :param length_equal: int: 长度必须等于指定的值（字符串，列表，元祖）
        :param length_range:
            tuple: 长度下限，上限（字符串，列表，元组）
            int:   长度下限，最少字符数（字符串，列表，元组）
        :param check_blank: bool: 是否检查空白符（False）
        :param blank_str: str: 空白符（需支持正则匹配）（默认为None,表示所有空白符）
        :param replace_or_raise: bool: 替换或抛异常, 默认抛异常（False）
        :param replace_str: str: 替换成的字符串，默认为空字符串（''）
        :param left_blank: bool: 仅匹配开头（False）
        :param right_blank: bool: 仅匹配结尾（False） 二者都为True表示同时匹配开头和结尾，二者都为False表示任意一处匹配
        :param file_check: bool: 是否校验文件（False）
        :param file_suffix: tuple: 文件后缀元组
        :param key_alias: str: 关键字别名
        :param regexp_str: str: 正则检验
        :param regexp_str_list: list: 多个正则检验
        :param regexp_message: str: 正则校验失败抛出的 message 信息
        :param without_check: bool: 是否检验（False）
        :param message: str: 错误信息（用户展示）
        :param save: bool: 是否存储（False）
        :param exc: Exception: 自定义异常类
        :return:
        """
        if without_check:  # 不检验
            return self[key] if key in self else default
        if key not in self:
            if must:  # 必传校验
                raise MissingParameters(ex_error=key if add_ex_error else None, msg=message)
            else:  # 非必传直接返回默认值
                if save:
                    self[key] = default
                return default
        val = self[key]
        # 类型校验
        val = type_vrf(key_alias or key, val, func=func, func_bak=func_bak, add_ex_error=add_ex_error,
                       message=message, exc=exc)
        # 范围校验
        val = range_vrf(key_alias or key, val, lt=lt, gt=gt, lte=lte, gte=gte, equal=equal, contains=contains,
                        non_equal=non_equal, non_contains=non_contains, add_ex_error=add_ex_error,
                        decimal_length=decimal_length, round_or_raise=round_or_raise, func_bak=func_bak,
                        length=length, length_equal=length_equal, length_range=length_range, message=message,
                        exc=exc)
        # 字符串空白符处理
        if check_blank and isinstance(val, str):
            val = blank_vrf(key_alias or key, val, add_ex_error=add_ex_error, blank_str=blank_str,
                            replace_or_raise=replace_or_raise, replace_str=replace_str, left_blank=left_blank,
                            right_blank=right_blank, message=message, exc=exc)

        # 字符串正则校验
        if regexp_str is not None:
            val = regexp_vrf(key_alias or key, val, regexp_str=regexp_str, add_ex_error=add_ex_error,
                             regexp_message=regexp_message or message, exc=exc)

        # 多个字符串正则校验
        if regexp_str_list is not None:
            val = regexp_vrf_list(key_alias or key, val, regexp_str_list=regexp_str_list, add_ex_error=add_ex_error,
                                  regexp_message=regexp_message or message, exc=exc)

        # 文件校验
        if file_check:
            file_vrf(key_alias or key, val, add_ex_error=add_ex_error, file_suffix=file_suffix, message=message,
                     exc=exc)

        # 存储
        if save:
            self[key] = val

        return val

    def update(self, dic):
        # super(Parameters, self).update(dic)
        # 只要遇到字典，都转化成Parameters
        dic = dict(dic)
        cp = SpecDeepcopy(Parameters)
        for k, v in dic.items():
            self[k] = cp.deepcopy(v)

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, val):
        self[key] = val

    def __hash__(self):
        return id(self)


def regexp_vrf(key, val, regexp_str, add_ex_error=True, regexp_message=None, exc=None):
    """

    :param key: str: 关键字名称
    :param val: any: 值
    :param regexp_str: str: 正则串
    :param add_ex_error: bool: 是否添加异常拓展信息
    :param regexp_message: str: 正则校验失败抛出的 message 信息
    :param exc: Exception: 自定义异常类
    :return: val
    """
    if isinstance(val, str) and re.search(regexp_str, val) is None:
        raise exc or ParamRegexpMatchFailed(ex_error=key if add_ex_error else None, msg=regexp_message)
    return val


def regexp_vrf_list(key, val, regexp_str_list, add_ex_error=True, regexp_message=None, exc=None):
    """针对多个不一样的正则字符串，只要有一个校验成功就返回（对于加盐参数是正确匹配的哪一个，接口里自己做区分，进而提取值）

    :param key: str: 关键字名称
    :param val: any: 值
    :param regexp_str_list: list: 正则串列表
    :param add_ex_error: bool: 是否添加异常拓展信息
    :param regexp_message: str: 正则校验失败抛出的 message 信息
    :param exc: Exception: 自定义异常类
    :return: val
    """
    for regexp_str in regexp_str_list:
        result_list = []
        if isinstance(val, str) and re.search(regexp_str, val) is None:
            result_list.append(0)
        else:
            result_list.append(1)
    if 1 not in result_list:
        raise exc or ParamRegexpMatchFailed(ex_error=key if add_ex_error else None, msg=regexp_message)
    return val


def type_vrf(key, val, func=None, func_bak=False, add_ex_error=True, message=None, exc=None):
    """类型校验
    :param key: str: 关键字名称
    :param val: any: 值
    :param func: func: 转换函数
    :param func_bak: bool: 是否返回转换后的值
    :param add_ex_error: bool: 是否添加异常拓展信息
    :param message: str: 错误信息（用户展示）
    :param exc: Exception: 自定义异常类
    :return: val
    """
    if func:
        try:
            func_bak_val = func(val)
        except Exception:
            raise exc or InvalidParamType(ex_error=key if add_ex_error else None, msg=message)
        if func_bak:
            val = func_bak_val
    return val


def range_vrf(key, val, lt=None, gt=None, lte=None, gte=None, equal=None,
              non_equal=None, non_contains=(), contains=(), add_ex_error=True,
              decimal_length=2, round_or_raise=True, func_bak=False, length=None,
              length_equal=None, length_range=None, message=None, exc=None):
    """范围校验
    :param key: str: 关键字名称
    :param val: any: 值
    :param lt: any: 小于
    :param gt: any: 大于
    :param lte: any: 小于等于
    :param gte: any: 大于等于
    :param equal: any: 等于比较
    :param non_equal: any: 不等于比较
    :param non_contains: any: not in 比较
    :param contains: seq: in比较
    :param add_ex_error: bool: 是否添加异常拓展信息
    :param decimal_length: int: 小数部分长度
    :param round_or_raise: bool: 四舍六入五成双（True）, 异常（False）
    :param func_bak: bool: 是否返回转换后的值
    :param length: int: 长度上限（字符串，列表，元祖）
    :param length_equal: int: 长度必须等于指定的值（字符串，列表，元祖）
    :param length_range:
        tuple: 长度下限，上限（字符串，列表，元祖）
        int:   长度下限，最少字符数（字符串，列表，元组）
    :param message: str: 错误信息（用户展示）
    :param exc: Exception: 自定义异常类
    :return: None
    """
    # 检验小数
    if isinstance(val, (PDecimal, Decimal, float)):
        new_val = PDecimal(val)
        if round_or_raise:  # 超出范围，四舍六入五成双
            new_val = round(val, decimal_length)
        else:  # 超出范围，直接报错
            pos = str(new_val).find('.')  # 小数点的下标
            if pos >= 0 and len(new_val) - pos - 1 > decimal_length:
                raise exc or InvalidParamRange(ex_error=key if add_ex_error else None, msg=message)  # 附加信息
            else:
                new_val = round(new_val, decimal_length)
        if func_bak:
            val = new_val
    # 范围校验
    if (lt is not None and not (val < lt)) or (gt is not None and not (val > gt)) \
            or (lte is not None and not (val <= lte)) or (gte is not None and not (val >= gte)) \
            or (equal is not None and val != equal) or (contains and not (val in contains)) \
            or (non_equal is not None and val == non_equal) or (non_contains and val in non_contains):
        raise exc or InvalidParamRange(ex_error=key if add_ex_error else None, msg=message)  # 附加信息
    # 长度校验
    if isinstance(val, (str, list, tuple)):
        if ((length is not None) and (not (len(val) <= length))) \
                or ((length_equal is not None) and (not (len(val) == length_equal))):
            raise exc or InvalidParamRange(ex_error=key if add_ex_error else None, msg=message)
        if length_range is not None:
            if isinstance(length_range, tuple):  # 上下限
                if not (length_range[0] <= len(val) <= length_range[1]):
                    raise exc or InvalidParamRange(ex_error=key if add_ex_error else None, msg=message)
            if isinstance(length_range, int):  # 下限
                if not (len(val) >= length_range):
                    raise exc or InvalidParamRange(ex_error=key if add_ex_error else None, msg=message)
    return val


def blank_vrf(key, val, add_ex_error=True, blank_str=None, replace_or_raise=False,
              replace_str='', left_blank=False, right_blank=False, message=None, exc=None):
    """空白符校验
    :param key: str: 关键字名称
    :param val: any: 值
    :param add_ex_error: bool: 是否添加异常拓展信息
    :param blank_str: str: 空白符（需支持正则匹配）
    :param replace_or_raise: bool: 替换或抛异常, 默认抛异常（False）
    :param replace_str: str: 替换成的字符串，默认为空字符串（''）
    :param left_blank: bool: 仅匹配开头（False）
    :param right_blank: bool: 仅匹配结尾（False） 二者都为True表示同时匹配开头和结尾
    :param message: str: 错误信息（用户展示）
    :param exc: Exception: 自定义异常类
    :return:
    """
    if not isinstance(val, str):  # 非字符串，直接返回
        return val
    if blank_str is None:
        blank_str = r'\s+'
    if left_blank and right_blank:
        blank_str = r'^' + blank_str + '|' + blank_str + '$'
    elif left_blank:
        blank_str = r'^' + blank_str
    elif right_blank:
        blank_str = blank_str + r'$'
    regex = re.compile(blank_str)
    if replace_or_raise:  # 替换
        return regex.sub(replace_str, val)
    else:  # 存在则抛异常
        if regex.search(val):
            raise exc or InvalidBlankParam(ex_error=key if add_ex_error else None, msg=message)
    return val


def file_vrf(key, val, add_ex_error=True, file_suffix=(), message=None, exc=None):
    """文件校验

    :param key:
    :param val:
    :param add_ex_error:
    :param file_suffix: tuple: 文件后缀元组
    :param message: str: 错误信息（用户展示）
    :param exc: Exception: 自定义异常类
    :return:
    """
    if not isinstance(val, (list, tuple, Iterator)):
        val = (val, )
    ex_error = key if add_ex_error else None
    for file in val:
        if not isinstance(file, UploadedFile):  # 仅接收这个类型的文件
            raise exc or InvalidFile(ex_error=ex_error, msg=message)
        if not file.name:  # 无文件名
            raise exc or MissingFileName(ex_error=ex_error, msg=message)
        if file_suffix and (not file.name.lower().endswith(file_suffix)):  # 不支持的文件格式
            raise exc or UnsupportedFileType(ex_error=ex_error, msg=message)
    return None
