# -*-coding:utf-8-*-

"""自定义DRF异常捕获，替换全局，异常在这里捕获"""

import logging
# from django.http import HttpResponse
from libs.utils.exception import ServerError, BaseError, UnsupportedMediaType
from libs.utils.error_code import ErrorCodeException
from rest_framework.exceptions import UnsupportedMediaType as UMTError
from libs.utils.response import ajax_fail

log = logging.getLogger(__name__)


def exception_handler(exc, context):
    """
    功能说明：自定义异常，替换DRF原生异常
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2020-11-10      new
    -------------------------------
    参数说明：
    :param exc: 捕获到的异常（认证异常, 接口业务逻辑异常）
    :param context: {'view': <apps.after_sales.views.RefundDtlView object at 0x000000000E0D4AC8>, 'args': (), 'kwargs': {}, 'request': <rest_framework.request.Request object at 0x000000000E110C50>}
    """
    if isinstance(exc, ErrorCodeException):  # 错误码异常
        return ajax_fail(ece=exc.ece, ece_msg=exc.message)
    elif isinstance(exc, UMTError):  # 媒体类型错误
        return ajax_fail(exc=UnsupportedMediaType())
    elif issubclass(exc.__class__, BaseError):  # 定义的子类
        return ajax_fail(exc=exc)
    log.exception(exc)
    return ajax_fail(exc=ServerError())

