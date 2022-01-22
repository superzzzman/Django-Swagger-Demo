# coding: utf-8
# author: zpt
from enum import IntEnum, unique, Enum


class BaseEnum(Enum):
    """
    功能说明：扩展枚举类
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-03-05     new
    -------------------------------
    """

    @classmethod
    def values(cls):
        return tuple(item.value for item in cls)


@unique
class UniqueIntEnum(BaseEnum, IntEnum):
    """
    功能说明：唯一整型枚举基类
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-03-05     new
    -------------------------------
    """
    pass
