# coding: utf-8

import logging
from . import wx_all, alipay_all
from ..old_payment.weixin.pay import WeixinPay
from alipay.aop.api.util import SignatureUtils

log = logging.getLogger(__name__)


class Data(dict):

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it.
        # Your __getattr__ is being called with "__getstate__" to find that magic method,
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val


def get_success(channel):
    if channel == "alipay":
        return "success"
    else:
        return WeixinPay().reply("OK", ok=True)


def get_data(request):
    """(旧版)阿里,微信不分"""
    try:
        class Data:
            pass

        data = Data()
        if request.POST.get("seller_id", ""):
            alipay_response = request.POST.copy()
            data.channel = "alipay"
            if alipay_response.get("trade_status", "fail") == "TRADE_SUCCESS":
                data.status = "success"
            else:
                data.status = "fail"
            data.order_no = alipay_response.get("out_trade_no", "")
            data.amount = alipay_response.get("total_amount", 0)
            data.seller_id = alipay_response.get("seller_id", "")
            data.sign = alipay_response.get("sign", "").encode("utf-8")
            data.body = alipay_response.get("body", "")
            alipay_response.pop("sign")
            alipay_response.pop("sign_type")
            data.original_string = SignatureUtils.get_sign_content(alipay_response).encode("utf-8")
        else:
            data.channel = "wx"
            wxUtils = WeixinPay()
            weixin_response = wxUtils.to_dict(request.body)
            if weixin_response.get("return_code", "fail") == "SUCCESS":
                data.status = "success"
            else:
                data.status = "fail"
            data.order_no = weixin_response.get("out_trade_no", "")
            data.amount = weixin_response.get("total_fee", 0)
            data.seller_id = weixin_response.get("mch_id", "")
            data.sign = weixin_response.pop("sign")
            data.body = weixin_response.get("attach", "")
            data.original_string = weixin_response
        return data
    except Exception as e:
        print(e)


def get_wx_callback_data(request):
    """获取微信支付回调数据"""
    wp_obj = WeixinPay()
    data = Data()
    try:
        res = wp_obj.to_dict(request.body)
    except Exception as e:
        log.error(e)
    if res.get("return_code", "") == "SUCCESS":
        data.status = "success"
    else:
        data.status = "fail"
    data.order_no = res.get("out_trade_no", "")  # 订单编号
    data.amount = res.get("total_fee", 0)
    data.seller_id = res.get("mch_id", "")
    data.sign = res.pop("sign")
    data.body = res.get("attach", "")
    data.original_string = res
    return data


def get_ali_callback_data(request):
    """获取阿里支付回调数据"""
    data = Data()
    res = request.POST.copy()
    data.channel = "alipay"
    if res.get("trade_status", "") in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        data.status = "success"
    else:
        data.status = "fail"
    data.order_no = res.get("out_trade_no", "")
    data.amount = res.get("total_amount", 0)
    data.seller_id = res.get("seller_id", "")
    data.sign = res.get("sign", "").encode("utf-8")
    data.body = res.get("body", "")
    res.pop("sign", None)
    res.pop("sign_type", None)
    data.original_string = SignatureUtils.get_sign_content(res).encode("utf-8")
    return data


def pay(subject, body, amount, order_no, channel, notify_url):
    """支付

    :param subject: str: 标题
    :param body: str: 内容
    :param amount: decimal.Decimal: 金额（小数部分保留到分）
    :param order_no: str: 订单编号
    :param channel: int: 支付渠道：1微信, 2阿里
    :param notify_url: str: 回调地址
    """
    if channel == 1:
        return wx_all.return_string_to_client(subject, amount, order_no, notify_url)
    elif channel == 2:
        return alipay_all.return_string_to_client(subject, body, amount, order_no, notify_url)
