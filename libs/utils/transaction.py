# coding: utf-8

"""事务相关"""

import logging
from functools import wraps
from django.db import transaction

log = logging.getLogger(__name__)


class AutoTransactionController(object):
    """
    功能说明：自动事务控制：自动提交/回滚
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    ld          2021-05-07         new
    ------------------------------------
    """

    __slots__ = ('_autocommit',)

    def __init__(self):
        self._autocommit = True

    def __enter__(self):
        self._autocommit = transaction.get_autocommit()
        transaction.set_autocommit(False)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type: obj: 异常类型
        :param exc_val: str: 异常值
        :param exc_tb: obj: 异常的错误栈信息
        """
        state = False
        if not exc_type:  # 不存在报错
            transaction.commit()
            state = True
        elif issubclass(exc_type, transaction.Error):  # 是django事务异常
            log.warning(exc_val)
            transaction.rollback()
            state = True
        else:  # 非django事务异常
            transaction.rollback()
        transaction.set_autocommit(self._autocommit)
        return state


def auto_transaction(func):
    """
    功能说明：自动事务控制装饰器
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    ld          2021-06-22         new
    ------------------------------------
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with AutoTransactionController():
            return func(*args, **kwargs)
    return wrapper
