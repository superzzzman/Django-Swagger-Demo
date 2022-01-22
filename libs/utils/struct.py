# coding: utf-8

"""公共"""

from collections import defaultdict
from decimal import Decimal

from django.core.paginator import Paginator
from django.db.models import Model


class NewStruct(dict):

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


class CallableKeyStruct(object):
    """可调用的带关键字的Struct"""

    __slots__ = ('struct_func', 'key', 'default_func')

    def __init__(self, key, default=None):
        self.struct_func = NewStruct
        self.key = key
        self.default_func = dict if default is None else default

    def __call__(self, *args, **kwargs):
        return self.struct_func(dic={self.key: self.default_func()})


class Info(object):

    __slots__ = ()

    def default_dict(self, type_=None):
        if type_ is None:
            return defaultdict(self.struct)
        return defaultdict(type_)

    @staticmethod
    def struct(dic=None, **kwargs):
        return NewStruct(dic, **kwargs)

    def callable_struct(self, key, default=None):
        """带关键字的struct
        :param key: str: 关键字
        :param default: Optional[TypeVar]:
        """
        if default is None:
            default = self.struct
        return CallableKeyStruct(key, default)

    def make_page(self, queryset, cur_page=1, per_page=10, data_list_key='dtoList'):
        """分页（带count）

        :param queryset: obj: QuerySet对象
        :param cur_page: int: 当前页号
        :param per_page: int: 每页显示数量
        :param data_list_key: str: 数据列表字段名
        :return: dict
        """
        info = self.struct()
        pages = Paginator(queryset, per_page)
        info.count = pages.count  # 总的记录数
        info.totalPages = pages.num_pages  # 总页数
        info.curPage = cur_page  # 当前页码
        info.perPage = per_page  # 每页数量
        info.initNum = per_page * (cur_page - 1)  # 起始记录数
        # 数据列表
        if (cur_page - 1) * per_page >= info.count:
            data_list = []
        else:
            data_list = [elem if isinstance(elem, Model) else self.struct(elem)
                         for elem in pages.get_page(cur_page).object_list]
        setattr(info, data_list_key, data_list)
        return info

    @staticmethod
    def make_page_without_count(qs, cur_page=1, per_page=10):
        """
        :param qs: QuerySet obj
        :param cur_page: int: 当前页号
        :param per_page: int: 每页显示数量
        """
        return qs[(cur_page - 1) * per_page: cur_page * per_page]

    @staticmethod
    def to_decimal(data, n=None):
        """转为自定义decimal类型
        :param data Any
        :param n: Optional[int]: 保留小数个数
        """
        data = Decimal(data)
        if n is not None:
            data = round(data, n)
        return data

    @staticmethod
    def distinct_with_old_sort(data):
        """按原顺序去重
        时间复杂度：O(n)
        空间复杂度：O(n)
        :param data: Union[List, Tuple]: 原始数据
        :return: list
        """
        tmp_set = set()
        new_data = []
        for elem in data:
            if elem in tmp_set:
                continue
            new_data.append(elem)
            tmp_set.add(elem)
        return new_data


base_info = Info()
