# coding=utf-8

import datetime
import decimal
import random
import uuid
import time
import string
import hashlib
from django.core.paginator import Paginator

# 不可删除，兼容老版本
from .verification_func import OneElem, StrToDatetime, SeqElemTransform, SmartCallStruct


class Struct(dict):
    """
    author lbl
    - 为字典加上点语法. 例如:
    >>> o = Struct({'a':1})
    >>> o.a
    >>> 1
    >>> o.b
    >>> None
    """
    def __init__(self, dictobj={}):
        self.update(dictobj)

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it. 
        # Your __getattr__ is being called with "__getstate__" to find that magic method, 
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val
    
    def __hash__(self):
        return id(self)


def make_page(queryset, per_page=10, cur_page=1):
    """
    功能说明：分页
    参数：queryset为查询集合
    --------------------------------
    修改人        修改时间       修改原因
    --------------------------------
    lbl        2019-8-12        new
    --------------------------------
    """
    data = Struct()
    pages = Paginator(queryset, per_page)
    data.count = pages.count  # 总的记录数
    data.num_pages = pages.num_pages  # 总页数
    data.cur_page = cur_page  # 当前页码
    data.init_num = per_page * (cur_page - 1)  # 起始记录数
    data.per_page = per_page        # 每页数量
    data.object_list = pages.get_page(cur_page).object_list if cur_page <= data.num_pages else []  # 当前页数据
    return data


class PDecimal(object):
    """
    功能说明：Decimal运算
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-07-09        new
    ld        2020-08-19        update（lt, gt）
    ld        2020-09-29        逻辑修改，初始化新增四舍六入五成双
    ld        2021-02-09        新增魔法方法：被减，被乘，被除
    --------------------------------
    """
    __slots__ = ('data', 'n')

    def __init__(self, data, n=None):
        """
        :param data: Decimal/str/int/float
        :param n: int: 四舍六入五成双，保留小数个数
        """
        self.data = data
        self.n = n
        self._init_handle()

    def _init_handle(self):
        """处理初始化数据

        :return:
        """
        if not isinstance(self.data, decimal.Decimal):
            self.data = self.decimald(self.data)
        if self.n is not None:
            self.data = round(self.data, self.n)

    @staticmethod
    def decimald(data):
        """decimal化"""
        if isinstance(data, PDecimal):
            return data.data
        if (data is None) or (data == ''):
            data = "0"
        elif isinstance(data, float):
            # float直接转Decimal精度不准确
            data = str(data)
        return decimal.Decimal(data)

    def __add__(self, other):
        """加"""
        other = self.decimald(other)
        return PDecimal(self.data + other, self.n)

    def __radd__(self, other):
        """被加"""
        return self.__add__(other)

    def __sub__(self, other):
        """减"""
        other = self.decimald(other)
        return PDecimal(self.data - other, self.n)

    def __rsub__(self, other):
        """被减"""
        other = self.decimald(other)
        return PDecimal(other - self.data, self.n)

    def __mul__(self, other):
        """乘"""
        other = self.decimald(other)
        return PDecimal(self.data * other, self.n)

    def __rmul__(self, other):
        """被乘"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """除"""
        other = self.decimald(other)
        return PDecimal(self.data / other, self.n)

    def __rtruediv__(self, other):
        """被除"""
        other = self.decimald(other)
        return PDecimal(other / self.data, self.n)

    def __floordiv__(self, other):
        """整除"""
        other = self.decimald(other)
        return PDecimal(self.data // other, self.n)

    def __rfloordiv__(self, other):
        """被整除"""
        other = self.decimald(other)
        return PDecimal(other // self.data, self.n)

    def __round__(self, n=0):
        return PDecimal(round(self.data, n))

    def __int__(self):
        return int(self.data)

    def __float__(self):
        return float(self.data)

    def __lt__(self, other):
        return self.data < self.decimald(other)

    def __le__(self, other):
        return self.data <= self.decimald(other)

    def __gt__(self, other):
        return self.data > self.decimald(other)

    def __ge__(self, other):
        return self.data >= self.decimald(other)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(str(self.data))


def make_uuid():
    """
    功能说明：生成uuid
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    lbl         2019-08-14         new
    """
    return str(uuid.uuid3(
        uuid.NAMESPACE_DNS,
        str(int(round(time.time() * 1000))) + ''.join(
            random.choices(string.digits, k=15)))).replace("-", "")[-24:]


def make_password(password, prefix):
    """
    功能说明：密码加密
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl      2019/08/16         new
    """
    salt = prefix + '~!@#$%^&*()_+147258369'
    password_new = password + salt
    obj = hashlib.md5(str(password_new).encode())
    return obj.hexdigest()


def transform_derived_table(seq, key_name='id', add_rn=False, rn_name='rn'):
    """
    参数示例：
    :param seq: 数据序列 List/Tuple/Generator等任意可迭代对象, 内部元素为str类型
    :param seq demo
        ['xxx1', 'xxx2', 'xxx3']
    :param key_name: 自定义的字段名
    :param add_rn: 是否添加行号
    :param rn_name: 行号字段名
    :returns: str
    :returns: demo
        "select 'xxx1' as id from dual union all ..."
        "select 1 as rn, 'xxx1' as id from dual union all ..."
    """
    if add_rn:
        return ''.join(f'union all select {i} as "{rn_name}", \'{item}\' as "{key_name}" from dual '
                       for i, item in enumerate(seq, start=1)).lstrip('union all')
    return ''.join(f'union all select \'{item}\' as "{key_name}" from dual '
                   for item in seq).lstrip('union all')


class NewStruct(dict):
    """
    功能说明：新版结构体，支持关键字参数
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-03-02         new
    --------------------------------
    """

    def __init__(self, dic=None, **kwargs):
        """
        :param dic: Union[dict, None]
        """
        if dic is not None:
            self.update(dic)
        if kwargs:
            self.update(kwargs)

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it.
        # Your __getattr__ is being called with "__getstate__" to find that magic method,
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val

    def __hash__(self):
        return id(self)
