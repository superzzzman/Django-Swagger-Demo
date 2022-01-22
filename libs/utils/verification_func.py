# coding: utf-8

import datetime
from collections.abc import Iterable


class OneElem(object):
    """
    功能说明：只存一个元素（最大或最小）
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2020-09-09         new
    --------------------------------
    """

    __slots__ = ('_elem', '_small_or_large')

    def __init__(self, small_or_large=True):
        """
        :param small_or_large: bool: True只存最小值，False只存最大值
        """
        self._elem = None  # 数据
        self._small_or_large = small_or_large

    def put(self, elem):
        """放入"""
        if self._elem is None:
            self._elem = elem
        elif self._small_or_large:  # 只存最小值
            self._elem = self._elem if self._elem <= elem else elem
        else:  # 只存最大值
            self._elem = self._elem if self._elem >= elem else elem

    @property
    def elem(self):
        if self._elem is None:
            return None
        return self._elem


class SeqElemTransform(object):
    """
    功能说明：序列元素类型转换
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2020-09-09         new
    --------------------------------
    使用说明：
        1.self.body.get中
            self.body.get('skuIds', [], func=SeqElemTransform(func=str), func_back=True)
        2.一般
            lst = [1, 'asd', 2]
            lst2 = SeqElemTransform(func=str)(lst)  # ['1', 'asd', '2']
    """

    __slots__ = ('_func', '_back', '_not_in')

    def __init__(self, func=str, back=list, not_in=(None, '')):
        """

        :param func: func: 内部元素转换类型
        :param back: func: 返回的序列类型
        """
        self._func = func
        self._back = back
        self._not_in = not_in

    def __call__(self, seq):
        for items in seq:
            if items in self._not_in:
                raise ValueError
        return self._back(self._func(items) for items in seq)


class StrToDatetime(object):
    """
    功能说明：字符串转日期
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2020-09-21         new
    --------------------------------
    使用说明：
        1.self.body.get中
            self.body.get('startTime', func=StrToDatetime(), func_back=True)
        2.一般
            end_time = '2020-02-02'
            end_time = StrToDatetime(add_days=1)(end_time)  # datetime.datetime(2020, 2, 3, 0, 0, 0)
    """

    def __init__(self, date_fmt='%Y-%m-%d', add_days=0):
        """

        :param date_fmt: str: 格式化字符串
        :param add_days: int: 追加天数
        """
        self.date_fmt = date_fmt
        self.add_days = add_days

    def __call__(self, data):
        data = datetime.datetime.strptime(data, self.date_fmt)
        if self.add_days:
            data += datetime.timedelta(days=self.add_days)
        return data


class SmartCallStruct(object):
    """智能调用结构体
    功能说明：支持延迟调用，传递参数
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-02-25         new
    --------------------------------
    """

    __slots__ = ('_func', '_args', '_kwargs')

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self, data):
        if self._args:
            return self._func(data, *self._args)
        elif self._kwargs:
            return self._func(data, **self._kwargs)
        return self._func(data)


class SeqSuperset:
    """
    功能说明：序列超集
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-05-26         new
    --------------------------------
    """

    __slots__ = ('_seq', '_nullable')

    @staticmethod
    def check_sequence(data):
        """检验序列

        :param data: Iterable: 可迭代对象
        :return:
        """
        if not isinstance(data, Iterable):
            raise ValueError
        return data

    def __init__(self, seq, nullable=True):
        """

        :param seq: Iterable: 可迭代对象
        :param nullable: bool: 是否允许为空序列
        """

        self._seq = set(self.check_sequence(seq))
        self._nullable = nullable

    def __contains__(self, seq):
        """in 魔法方法

        :param seq: Iterable: 可迭代对象
        :return:
        """
        seq = self.check_sequence(seq)
        if (not self._nullable) and (not seq):
            return False
        for elem in seq:
            if elem not in self._seq:
                return False
        return True


class NotMustTransFunc:
    """
    功能说明：非必转换
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-06-09         new
    --------------------------------
    """

    __slots__ = ('_func', '_non_trans_value')

    def __init__(self, func, non_trans_value=''):
        self._func = func
        self._non_trans_value = non_trans_value

    def __call__(self, val):
        if val == self._non_trans_value:
            return val
        return self._func(val)


class SpecifyTransValue:
    """
    功能说明：指定转换成某个值
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-09-10         new
    --------------------------------
    """

    __slots__ = ("_func", "_spec_value", "_val", "_val_seq")

    def __init__(self, func, val, spec_value=None, val_seq=()):
        """
        :param func: Callable: 方法
        :param spec_value: Any: 指定的值
        :param val: Any: 匹配的值
        :param val_seq: Sequence[Any]: 匹配的值的序列
        """
        self._func = func
        self._spec_value = spec_value
        self._val = val
        self._val_seq = val_seq

    def __call__(self, val):
        if val == self._val or val in self._val_seq:
            return self._spec_value
        return self._func(val)
