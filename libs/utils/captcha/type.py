# coding: utf-8

"""验证码类型"""

from typing import NamedTuple
from types import DynamicClassAttribute
from enum import Enum

from libs.utils.enum import BaseEnumMeta, keyword_value_unique

__all__ = (
    'CaptchaTypeData',
    'CaptchaTypeBaseEnum'
)


class CaptchaTypeData(NamedTuple):
    """验证码类型数据"""
    val: int      # 值
    keyword: str  # 关键字
    timeout: int  # 超时时间（秒）


class _CaptchaTypeEnumMeta(BaseEnumMeta):
    """验证码类型枚举元类"""

    def __new__(mcs, *args, **kwargs):
        enum_class = super(_CaptchaTypeEnumMeta, mcs).__new__(mcs, *args, **kwargs)
        # 唯一性校验
        enum_class = keyword_value_unique(('val', 'keyword'))(enum_class)
        # 成员val->Enum的映射
        enum_class._member_val_map_ = {enum.value.val: enum for enum in enum_class}
        return enum_class

    @property
    def values(cls):
        return tuple(cls._member_val_map_.keys())

    def get_enum_by_val(cls, val: int):
        """通过val获取对应的enum对象"""
        return cls._member_val_map_[val]


class CaptchaTypeBaseEnum(Enum, metaclass=_CaptchaTypeEnumMeta):
    """验证码类型枚举基类

    使用示例：
    class CaptchaTypeEnum(CaptchaTypeBaseEnum):
        TYPE1 = CaptchaTypeData(val1: int, keyword1: str, timeout1: int)
        TYPE2 = CaptchaTypeData(val2: int, keyword2: str, timeout2: int)

    1.已知成员的val，获取对应的enum对象
    val = 1
    enum = CaptchaTypeEnum.get_enum_by_val(val)

    2.获取成员的数据
    enum = CaptchaTypeEnum.TYPE1
    enum.val
    enum.keyword
    enum.timeout
    """

    @DynamicClassAttribute
    def val(self):
        """值"""
        return self.value.val

    @DynamicClassAttribute
    def keyword(self):
        """关键字：缓存中使用"""
        return self.value.keyword

    @DynamicClassAttribute
    def timeout(self):
        """超时时间（秒）"""
        return self.value.timeout
