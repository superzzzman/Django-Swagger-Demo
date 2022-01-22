# -*-coding:utf-8-*-

"""短信相关"""

import json

from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_msg(phone: str, template_code: str, template_params: dict):
    """
    功能说明：发送短信
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl      2019/09/16         new

    :param phone: 手机号
    :param template_code: 模板代码
    :param template_params: 模板参数
    """
    client = AcsClient(settings.ACCESS_KEY_ID_MSG, settings.ACCESS_KEY_SECRET_MSG, 'default')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', 'default')
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', settings.SMS_SIGN_NAME)
    request.add_query_param('TemplateCode', template_code)
    request.add_query_param('TemplateParam', json.dumps(template_params))
    response = client.do_action_with_exception(request)
    return json.loads(response)
