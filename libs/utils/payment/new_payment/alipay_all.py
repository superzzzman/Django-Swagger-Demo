# coding: utf-8

import logging

from django.conf import settings

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest

log = logging.getLogger(__name__)


def return_string_to_client(subject, body, amount, order_no, notify_url):
    """

    :param subject: str: 标题
    :param body: str: 内容
    :param amount: decimal.Decimal: 金额
    :param order_no: str: 订单编号
    :param notify_url: str: 回调地址
    """
    alipay_client_config = AlipayClientConfig()
    # alipay_client_config.server_url = Setting.gateway
    alipay_client_config.app_id = settings.ALIPAY_APP_ID
    alipay_client_config.app_private_key = settings.ALIPAY_PRIVATE_KEY
    alipay_client_config.alipay_public_key = settings.ALIPAY_PUBLIC_KEY

    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    model = AlipayTradeAppPayModel()
    model.timeout_express = "60m"
    model.total_amount = str(amount)
    model.body = body
    model.product_code = "QUICK_MSECURITY_PAY"
    model.subject = subject
    model.out_trade_no = order_no
    request = AlipayTradeAppPayRequest(biz_model=model)
    request.notify_url = notify_url
    response = client.sdk_execute(request)
    return {'urlParams': response}
