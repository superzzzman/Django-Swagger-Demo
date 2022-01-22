# coding: utf-8

import logging
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import UnsupportedMediaType as UMTError
from libs.utils.exception import UnsupportedMediaType, ServerError, BaseError
from libs.utils.response import ajax_fail

log = logging.getLogger(__name__)


class ExceptionMiddleware(MiddlewareMixin):
    """
    功能说明：异常捕获中间件
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2020-11-10      new
    --------------------------------
    """

    @staticmethod
    def process_exception(request, exc):
        if isinstance(exc, UMTError):  # 不支持的媒体类型
            return ajax_fail(exc=UnsupportedMediaType())
        elif issubclass(exc.__class__, BaseError):  # 定义的子类
            return ajax_fail(exc=exc)
        log.exception(exc)
        return ajax_fail(exc=ServerError())

