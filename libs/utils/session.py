# -*-coding:utf-8-*-

import datetime
from django.contrib.sessions.models import Session


class SessionHandler(object):
    """
    功能说明：验证session是否存在
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-09-02        new
    ld        2021-03-02        逻辑优化
    --------------------------------
    """

    __slots__ = ()

    @staticmethod
    def expired_by_key(session_key):
        """使指定的session过期"""
        now = datetime.datetime.now()
        Session.objects.filter(session_key=session_key, expire_date__gt=now).update(expire_date=now)

    @staticmethod
    def expired_by_user_id(user_id):
        """使指定的用户的session过期"""
        now = datetime.datetime.now()
        Session.objects.extra(where=[f"user_id = '{user_id}'"]) \
            .filter(expire_date__gt=now).update(expire_date=now)

    @staticmethod
    def is_owner(session_key, user_id):
        """检验session_key和user_id是否一致"""
        state = Session.objects.extra(where=[f"user_id = '{user_id}'"]) \
            .filter(session_key=session_key).exists()
        return bool(state)

