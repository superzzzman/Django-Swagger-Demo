# coding: utf-8

import datetime
import logging
from django.shortcuts import reverse
from urllib.parse import urljoin
from ..old_payment.weixin.pay import WeixinPay, WeixinPayError
from datetime import timedelta, datetime
from django.conf import settings

log = logging.getLogger(__name__)


class Setting(object):
    app_id = settings.WXPAY_APP_ID
    mch_id = settings.WXPAY_MCH_ID
    mch_key = settings.WXPAY_MCH_KEY
    trade_type = "APP"

    def __init__(self, arg):
        super(Setting, self).__init__()
        self.arg = arg


def return_string_to_client(subject, amount, order_no, notify_url):
    """
    :param subject: str: 标题
    :param amount: decimal.Decimal: 金额
    :param order_no: str: 订单编号
    :param notify_url: str: 回调地址
    """
    nowtime = str(int((datetime.utcnow() + timedelta(hours=8)).timestamp()))[0:10]
    # amount = round(float(amount) * 100)
    amount = int(amount * 100)
    pay = WeixinPay(Setting.app_id, Setting.mch_id, Setting.mch_key, notify_url)
    try:
        response = pay.unified_order(
            body=subject,
            out_trade_no=order_no,
            total_fee=amount,
            product_id="",
            trade_type=Setting.trade_type,
            attach=subject
        )
        print()
        response["sign"] = pay.sign(
            dict(appid=Setting.app_id, partnerid=Setting.mch_id, prepayid=response["prepay_id"], package="Sign=WXPay",
                 noncestr=response["nonce_str"], timestamp=nowtime))
        response["timestamp"] = nowtime
        response["package"] = "Sign=WXPay"
        response["partnerid"] = Setting.mch_id
        response["app_id"] = Setting.app_id
        return response
    except WeixinPayError as e:
        log.error(e)
