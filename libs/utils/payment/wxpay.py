# coding: utf-8

"""微信支付相关"""

from __future__ import annotations

from decimal import Decimal
from typing import Optional, Any

from django.conf import settings

from .old_payment.weixin.pay import WeixinPay, WeixinPayError
from libs.utils.logger import LoggerProxy

logger = LoggerProxy(__name__)


def get_wx_qrcode(body: str, trade_no: str, fee: Decimal, notify_url: str, time_expire: Optional[str] = None,
                  trade_type: str = "NATIVE", product_id: str = ""):
    """

    :param body: str: 内容
    :param trade_no: str: 支付单号，自己创建，不允许重复
    :param fee: Decimal: 金额浮点字符串，小数点后两位（最小分） 如：1分 "0.01"
    :param trade_type: str: 支付类型
    :param notify_url: str: 回调地址
    :param time_expire: str: 交易结束时间
        订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010
    :param product_id: str: 商品id，必填
    :return:
    """
    pay_obj = WeixinPay(app_id=settings.WXPAY_APP_ID, mch_id=settings.WXPAY_MCH_ID, mch_key=settings.WXPAY_MCH_KEY,
                        notify_url=notify_url)
    # 截取整数部分保留未字符串
    fee = str(int(Decimal(fee) * 100))
    data: dict[str, Any] = {}
    data.setdefault("body", body)
    data.setdefault("out_trade_no", trade_no)
    data.setdefault("total_fee", fee)
    data.setdefault("trade_type", trade_type)
    data.setdefault("product_id", product_id)
    if time_expire is not None:
        data.setdefault("time_expire", time_expire)
    try:
        response = pay_obj.unified_order(**data)
    except Exception as e:
        logger.error(e)
        return None
    if response.get('return_code') != 'SUCCESS':
        logger.error(response)
        return None
    return response.get('code_url')


def close_wx_order(order_no: str) -> bool:
    """关闭微信订单

    :param order_no: 订单编号
    """
    pay_obj = WeixinPay(app_id=settings.WXPAY_APP_ID, mch_id=settings.WXPAY_MCH_ID, mch_key=settings.WXPAY_MCH_KEY)
    try:
        response = pay_obj.close_order(out_trade_no=order_no)
    except WeixinPayError as e:
        # 异常： https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3
        logger.warning(e)
        return False
    if response.get("return_code") != "SUCCESS":
        logger.error(response)
        return False
    return True
