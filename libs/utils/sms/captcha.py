# coding: utf-8

"""短信验证码"""

import logging
from enum import Enum, unique
from typing import Dict

from . import send_msg
from libs.utils.error_code import ECEnum, ECException

log = logging.getLogger(__name__)


@unique
class SMSTypeEnum(Enum):
    """短信类型"""
    CAPTCHA = 'captcha'  # 验证码


def check_sms_response(response: dict, phone: str, type_enum: SMSTypeEnum) -> None:
    """检验短信服务响应

    :param response: 响应
    :param phone: 手机号
    :param type_enum: 短信类型枚举
    """
    res_code = response.get('Code')
    if res_code != 'OK':
        if res_code == "isv.BUSINESS_LIMIT_CONTROL":
            msg = '短信发送频率超限, 请稍后重试'
        elif res_code == "sv.MOBILE_NUMBER_ILLEGAL":
            msg = '手机号码格式错误'
        elif res_code == "isv.DAY_LIMIT_CONTROL":
            msg = '当日可发送验证码已达上限'
        else:
            msg = '验证码发送失败'
            log.error(f"phone <{phone}> send <{type_enum.value}> failed, response: {response}")
        raise ECException(ECEnum.SMSServerError, message=msg)
    return None


def send_sms_captcha(phone: str, captcha: str, tp: int) -> None:
    """发送短信验证码
    tp: 类型： 1注册, 2修改密码
    """
    # 模板code
    template_code: str
    # 模板参数
    template_params: Dict[str, str]
    # 短信类型枚举
    sms_type_enum: SMSTypeEnum = SMSTypeEnum.CAPTCHA
    if tp == 1:  # 注册
        template_code = 'SMS_217845055'
        template_params = {"code": captcha}
    else:
        template_code = 'SMS_217845055'
        template_params = {"code": captcha}
    response = send_msg(phone=phone, template_code=template_code, template_params=template_params)
    return check_sms_response(response, phone, sms_type_enum)
