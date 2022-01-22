# coding: utf-8

"""拷贝相关"""

from copy import deepcopy


class SpecDeepcopy(object):
    """
    功能说明：特色深拷贝
    --------------------------------
    修改人      修改时间        修改原因
    --------------------------------
    ld        2021-05-06        new
    --------------------------------
    """

    __slots__ = ('_dict_type',)

    def __init__(self, dict_type=None):
        """
        :param dict_type: type: 字典类
        """
        self._dict_type = dict_type or dict

    def deepcopy(self, seq):
        if isinstance(seq, dict):
            seq = self._copy_dict(seq)
        elif isinstance(seq, list):
            seq = self._copy_list(seq)
        elif isinstance(seq, tuple):
            seq = self._copy_tuple(seq)
        elif isinstance(seq, set):
            seq = self._copy_set(seq)
        else:
            seq = seq
        return seq

    def _copy_dict(self, seq):
        data = self._dict_type()
        if seq:
            for k, v in seq.items():
                data[k] = self.deepcopy(v)
        return data

    def _copy_list(self, seq):
        data = []
        if seq:
            for i in seq:
                data.append(self.deepcopy(i))
        return data

    def _copy_tuple(self, seq):
        data = []
        if seq:
            for i in seq:
                data.append(self.deepcopy(i))
        data = tuple(data)
        return data

    def _copy_set(self, seq):
        data = set()
        if seq:
            for i in seq:
                data.add(self.deepcopy(i))
        return data

