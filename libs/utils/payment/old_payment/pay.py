# coding:utf-8
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from alipay.aop.api.util import SignatureUtils
from .weixin.pay import WeixinPay
from . import alipay_all
from . import wx_all
from libs.models.models import PayLog
from libs.utils.ajax import ajax_fail
from libs.utils.ajax import ajax_ok
from datetime import datetime, timedelta
import os
import logging

log = logging.getLogger(__name__)
current_dir = os.path.dirname(os.path.realpath(__file__))


def getSuccess(channel):
    if channel == "alipay":
        return "success"
    else:
        return WeixinPay().reply("OK", ok=True)


def get_pay_seller_id(channel):
    if channel == "alipay":
        return "2088721470032523"
    else:
        return "1489365792"


def get_data(request):
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


def get_fee(channel, amount):
    if channel == "alipay":
        return round(float(amount) * 100)
    else:
        return float(amount)


def verify(channel, original_string, sign):
    if channel == "alipay":
        with open(os.path.join(current_dir, "alipay_public_key.pem")) as fp:
            alipay_public_key = fp.read()
        return SignatureUtils.verify_with_rsa(alipay_public_key, original_string, sign)
    else:
        return sign == WeixinPay(mch_key="8Z7xC8dG25od3lvkUVy3JvApHLEZWwB5").sign(original_string)


def change_top_up_virtual(charge_id):
    """
    设置充值状态
    :return:
    """
    PayLog.objects.filter(pay_log_id=charge_id).update("status=-1", update_time=datetime.now())
    return ajax_fail(error=684, message='支付失败')


def pay(subject="", body="", amount="", order_no="", channel=""):
    if channel == "wx":
        return wx_all.return_string_to_client(subject, body, amount, order_no)
    else:
        return alipay_all.return_string_to_client(subject, body, amount, order_no)


@csrf_exempt
def pay_success_notify_new(request):
    """
    功能说明：支付成功回调
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl     2020-07-14         new
    -------------------------------
    """
    try:
        data = get_data(request)
        pay_channel = data.channel
        pay_status = data.status
        pay_order_no = data.order_no
        pay_seller_id = data.seller_id
        pay_sign = data.sign
        pay_original_string = data.original_string
        if not verify(pay_channel, pay_original_string, pay_sign):
            return HttpResponse(getSuccess(pay_channel))
        if pay_status != "success":
            log.exception('订单支付回调异常', extra=dict(req=request))
            return HttpResponseServerError("fail")
        if pay_seller_id != get_pay_seller_id(pay_channel):
            return HttpResponse(getSuccess(pay_channel))
        # 支付成功后相关业务逻辑处理
        try:
            pay_log = PayLog.objects.filter(pay_id=pay_order_no)\
                .values("type", "pay_id", "pay_type", "user_id", "count", "price", "voucher_show_id").first()
            # if pay_log.get("type") == 0:        # 处理订单
            #     handle_order_info(pay_log, request)
            # elif pay_log.get("type") == 1:      # 潮钱
            #     handle_tide_money_info(pay_log, request)
            # elif pay_log.get("type") == 2:      # vip
            #     handle_vip_info(pay_log, request)
        except Exception as e:
            log.exception('订单支付回调处理业务异常：pay_id:' + pay_order_no, extra=dict(req=request))
        return HttpResponse(getSuccess(pay_channel))
    except Exception as e:
        log.exception('订单支付回调异常', extra=dict(req=request))
        return HttpResponseServerError(e)


def get_num_float(num, places):
    """
    功能说明：保留小数位数（不四舍五入）
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    lbl     2020-07-15         new
    -------------------------------
    """
    integer, point, decimals = str(num).partition('.')
    decimals = (decimals + "0" * places)[:places]
    return float(".".join([integer, decimals]))

