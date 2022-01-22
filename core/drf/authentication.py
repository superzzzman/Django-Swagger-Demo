# coding: utf-8

"""自定义DRF认证"""

import datetime

from rest_framework.authentication import BaseAuthentication

from apps.models import UserToken
from libs.utils.jwt import jwt_decode
from libs.utils.error_code import ECException, ECEnum


class TokenAuth(BaseAuthentication):
    """
    功能说明：token认证
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2021-08-04        new
    --------------------------------
    """

    def authenticate(self, request):
        now = datetime.datetime.now()
        token = request.headers.get('token')
        # 校验token
        queryset = UserToken.objects.filter(token=token, status=1, expire_time__gt=now)
        if not queryset.exists():  # 过期
            raise ECException(ECEnum.TokenExpiredOrNotExist)
        user_id = jwt_decode(token).get('user_id')
        return user_id, token

    def authenticate_header(self, request):
        pass
