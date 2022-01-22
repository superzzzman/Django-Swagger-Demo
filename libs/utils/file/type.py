# coding: utf-8

"""文件类型"""

from typing import NamedTuple, Tuple
from types import DynamicClassAttribute
from enum import Enum, unique

from libs.utils.enum import BaseEnumMeta, keyword_value_unique

__all__ = (
    'FileTypeData',
    'FileTypeBaseEnum',
    'FileCategoryData',
    'FileCategoryBaseEnum',
)


class FileTypeData(NamedTuple):
    """文件类型数据"""
    val: int                   # 值
    path: str                  # 路径
    suffixes: Tuple[str, ...]  # 允许的后缀


class FileCategoryData(NamedTuple):
    """文件分类数据"""
    val: int       # 值
    keyword: str   # 关键字


class _FileTypeEnumMeta(BaseEnumMeta):
    """文件类型枚举元类"""

    def __new__(mcs, *args, **kwargs):
        enum_class = super(_FileTypeEnumMeta, mcs).__new__(mcs, *args, **kwargs)
        # 唯一性校验
        enum_class = keyword_value_unique(('val', 'path'))(enum_class)
        # 成员val->Enum的映射
        enum_class._member_val_map_ = {enum.value.val: enum for enum in enum_class}
        return enum_class

    @property
    def values(cls):
        return tuple(cls._member_val_map_.keys())

    def get_enum_by_val(cls, val: int):
        """通过val获取对应的enum对象"""
        return cls._member_val_map_[val]


class _FileCategoryEnumMeta(BaseEnumMeta):
    """文件分类枚举元类"""

    def __new__(mcs, *args, **kwargs):
        enum_class = super(_FileCategoryEnumMeta, mcs).__new__(mcs, *args, **kwargs)
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


class FileTypeBaseEnum(Enum, metaclass=_FileTypeEnumMeta):
    """文件类型枚举基类

    使用示例：
    class FileTypeEnum(FileTypeBaseEnum):
        TYPE1 = CaptchaTypeData(val1: int, path: str, suffixes: Tuple[str, ...])

    """

    @DynamicClassAttribute
    def val(self) -> int:
        """值"""
        return self.value.val

    @DynamicClassAttribute
    def path(self) -> str:
        """关键字：缓存中使用"""
        return self.value.path

    @DynamicClassAttribute
    def suffixes(self) -> Tuple[str, ...]:
        """超时时间（秒）"""
        return self.value.suffixes


class FileCategoryBaseEnum(Enum, metaclass=_FileCategoryEnumMeta):
    """文件分类枚举基类

    使用示例
    class FileCategoryEnum(FileCategoryBaseEnum):
        TYPE1 = CaptchaTypeData(val1: int, keyword: str)

    """

    @DynamicClassAttribute
    def val(self) -> int:
        """值"""
        return self.value.val

    @DynamicClassAttribute
    def keyword(self) -> int:
        """关键字"""
        return self.value.keyword
