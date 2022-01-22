# coding: utf-8

import json
from decimal import Decimal
from typing import Optional

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipayTradePrecreateRequest import AlipayTradePrecreateRequest
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeCloseRequest import AlipayTradeCloseRequest
from alipay.aop.api.domain.AlipayTradeCloseModel import AlipayTradeCloseModel
from django.conf import settings

from libs.utils.logger import LoggerProxy

logger = LoggerProxy(__name__)


def get_ali_client_config() -> AlipayClientConfig:
    """获取阿里客户端配置"""
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.app_id = settings.ALIPAY_APP_ID
    alipay_client_config.app_private_key = settings.ALIPAY_PRIVATE_KEY
    alipay_client_config.alipay_public_key = settings.ALIPAY_PUBLIC_KEY
    return alipay_client_config


def get_ali_qrcode(subject: str, order_no: str, fee: Decimal, notify_url: str,
                   timeout_express: Optional[str] = None, body: str = ""):
    """阿里支付二维码

    :param subject: 标题
    :param order_no: 订单id
    :param fee: 费用字符串，小数点后两位（分）
    :param notify_url: 回调地址
    :param timeout_express: 相对超时时间
        订单相对超时时间。
        该笔订单允许的最晚付款时间，逾期将关闭交易。
        取值范围：1m～15d。m-分钟，h-小时，d-天，1c-当天（1c-当天的情况下，无论交易何时创建，都在0点关闭）。
        该参数数值不接受小数点， 如 1.5h，可转换为 90m。
        当面付场景默认值为3h；
        其它场景默认值为15d;
    :param body: ...
    """

    alipay_client_config = get_ali_client_config()
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    model = AlipayTradeAppPayModel()
    model.timeout_express = "60m"
    model.total_amount = str(fee)
    model.body = body
    model.product_code = "FACE_TO_FACE_PAYMENT"
    model.subject = subject
    model.out_trade_no = order_no
    model.timeout_express = timeout_express
    request = AlipayTradePrecreateRequest(biz_model=model)
    request.notify_url = notify_url
    response = json.loads(client.execute(request))
    if response['code'] != '10000':
        logger.error(response)
        return None
    return response['qr_code']


def close_ali_order(order_no: str) -> bool:
    """关闭阿里订单"""

    alipay_client_config = get_ali_client_config()
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    model = AlipayTradeCloseModel()
    model.out_trade_no = order_no
    request = AlipayTradeCloseRequest(biz_model=model)
    response = json.loads(client.execute(request))
    # print(response)
    if response["code"] != "10000":
        logger.warning(response)
        return False
    return True
