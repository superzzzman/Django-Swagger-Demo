import os
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from django.http import HttpResponse
from django.conf import settings
import logging
import json
log = logging.getLogger(__name__)


class Setting(object):
    gateway = "https://openapi.alipay.com/gateway.do"
    app_id = "2017072107834558"
    # gateway = "https://openapi.alipaydev.com/gateway.do"
    # app_id = "2016092400584972"
    current_dir = os.path.dirname(os.path.realpath(__file__))
    app_alipay_private_key = os.path.join(current_dir, "app_alipay_private_key.pem")
    alipay_public_key = os.path.join(current_dir, "alipay_public_key.pem")

    notify_url = "%s/chaoxingqiu/goods/pay/success/" % settings.BASE_PATH

    with open(app_alipay_private_key) as fp:
        app_alipay_private_key = fp.read()
    with open(alipay_public_key) as fp:
        alipay_public_key = fp.read()

    def __init__(self, arg):
        super(Setting, self).__init__()
        self.arg = arg


def return_string_to_client(subject, body, amount, order_no):
    # try:
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = Setting.gateway
    alipay_client_config.app_id = Setting.app_id
    alipay_client_config.app_private_key = Setting.app_alipay_private_key
    alipay_client_config.alipay_public_key = Setting.alipay_public_key

    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

    model = AlipayTradeAppPayModel()
    model.timeout_express = "60m"
    model.total_amount = str(amount)
    # model.count = count
    model.body = body
    model.product_code = "QUICK_MSECURITY_PAY"
    model.subject = subject
    model.out_trade_no = order_no
    request = AlipayTradeAppPayRequest(biz_model=model)
    request.notify_url = Setting.notify_url
    response = client.sdk_execute(request)
    return response
    # except Exception as e:
    #     print(e)
        # raise pay_error(e)

'''
request*20
STDOUT web1 16:30:14
<WSGIRequest: POST '/a/'>
STDOUT web1 16:30:14
META*20
STDOUT web1 16:30:14
{
	'CONTENT_LENGTH': '1199', 
	'SERVER_NAME': '::', 
	'wsgi.url_scheme': 'http', 
	'HTTP_X_REAL_IP': '203.209.233.205', 
	'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>, 
	'SERVER_PORT': '3000', 
	'HTTP_X_LC_DOMAIN': 'mengquapptest', 
	'QUERY_STRING': '', 
	'SERVER_PROTOCOL': 'HTTP/1.1', 
	'HTTP_USER_AGENT': 'Mozilla/4.0', 
	'HTTP_X_FORWARDED_PROTO': 'https', 
	'HTTP_X_AVOSCLOUD_CODE_WEB_HOSTING': '1', 
	'leanengine.request': <Request 'http://mengquapptest.leanapp.cn/a/' [POST]>, 
	'wsgi.run_once': False, 
	'HTTP_HOST': 'mengquapptest.leanapp.cn', 
	'REMOTE_ADDR': '::ffff:10.10.68.29', 
	'HTTP_CONNECTION': 'close', 
	'wsgi.multiprocess': False, 
	'REMOTE_PORT': '53078', 
	'werkzeug.request': <Request 'http://mengquapptest.leanapp.cn/a/' [POST]>, 
	'GATEWAY_INTERFACE': 'CGI/1.1', 
	'SCRIPT_NAME': '', 
	'CONTENT_TYPE': 'application/x-www-form-urlencoded; charset=utf-8', 
	'wsgi.multithread': False, 
	'REQUEST_METHOD': 'POST', 
	'SERVER_SOFTWARE': 'gevent/1.2 Python/3.5', 
	'wsgi.version': (1, 0), 
	'PATH_INFO': '/a/', 
	'wsgi.input': <gevent.pywsgi.Input object at 0x7f60a506e648>
}
STDOUT web1 16:30:14
body*20
STDOUT web1 16:30:14
gmt_create=2018-12-10+16%3A30%3A13&
charset=utf-8&
seller_email=postmaster%40meng2333.com&
subject=%E8%90%8C%E8%B6%A3%E8%AE%A2%E5%8D%95-5c0e240f808ca400723cc5c1x1&
sign=EfXmmvSuZ0JFSKYe6AjPr5Ud5HWOE7ZCnMx%2Fpgw8cix%2BqRiH1zCoz0oX1Cgc9vAniCqdIkiAT6rcByy86kkYczlJtLWnLZEBQwwx%2B4Cp%2F1wxjvkSIqpRgtMVu3Pp0XOlLmNx%2FhULwp1LBgQ5tONZBP2bjRWMhaeMmPp4aKMebv%2FclsCYaqwChLo23B4jHXtZxUo5zHnl1MKc4NaXVZC%2B5MKiyCK3nrcTDmXeN2PmBb5zj5xfoitNZsUk24eaSnx%2BoyluMDU6hJvIiAx25sgaY75CoULiUYaQM5J2s516a0rfvIM47BlIFF4uIWYQjsAzAllxaOobl0vjfubN%2BJHDLQ%3D%3D&
body=%E8%90%8C%E8%B6%A3%E8%AE%A2%E5%8D%95-5c0e240f808ca400723cc5c1x1&
buyer_id=2088412253142006&
invoice_amount=0.01&
notify_id=2018121000222163014042001040747894&
fund_bill_list=%5B%7B%22amount%22%3A%220.01%22%2C%22fundChannel%22%3A%22PCREDIT%22%7D%5D&
notify_type=trade_status_sync&
trade_status=TRADE_SUCCESS&
receipt_amount=0.01&
app_id=2017072107834558&
buyer_pay_amount=0.01&
sign_type=RSA2&
seller_id=2088721470032523&
gmt_payment=2018-12-10+16%3A30%3A14&
notify_time=2018-12-10+16%3A30%3A14&
version=1.0&
out_trade_no=5c0e240f808ca400723cc5c1x1&
total_amount=0.01&
trade_no=2018121022001442001019950145&
auth_app_id=2017072107834558&
buyer_logon_id=183****6574&point_amount=0.00
'''

"""
   带文件的系统接口示例：alipay.offline.material.image.upload
   """