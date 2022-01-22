from .weixin.pay import WeixinPay, WeixinPayError
from datetime import timedelta, datetime
from django.conf import settings


class Setting(object):
    app_id = "wxed3467f6c5d18070"
    mch_id = "1489365792"
    mch_key = "8Z7xC8dG25od3lvkUVy3JvApHLEZWwB5"
    notify_url = "%s/chaoxingqiu/goods/pay/success/" % settings.BASE_PATH
    trade_type = "APP"

    def __init__(self, arg):
        super(Setting, self).__init__()
        self.arg = arg


def return_string_to_client(subject, body, amount, order_no):
    nowtime = str(int((datetime.utcnow() + timedelta(hours=8)).timestamp()))[0:10]
    amount = round(float(amount) * 100)
    pay = WeixinPay(
        Setting.app_id,
        Setting.mch_id,
        Setting.mch_key,
        Setting.notify_url,
    )
    try:
        response = pay.unified_order(
            body=body,
            out_trade_no=order_no,
            total_fee=amount,
            product_id="",
            trade_type=Setting.trade_type,
            attach=body
        )

        response["sign"] = pay.sign(
            dict(appid=Setting.app_id, partnerid=Setting.mch_id, prepayid=response["prepay_id"], package="Sign=WXPay",
                 noncestr=response["nonce_str"], timestamp=nowtime))
        response["timestamp"] = nowtime
        response["package"] = "Sign=WXPay"
        response["partnerid"] = Setting.mch_id
        response["app_id"] = Setting.app_id
        return response
    except Exception as e:
        print(e)
# return_string_to_client(body=, amount=, order_no=)

'''
request*20
STDOUT web1 19:57:27
<WSGIRequest: POST '/a/'>
STDOUT web1 19:57:27
META*20
STDOUT web1 19:57:27
{
	'wsgi.version': (1, 0), '
	wsgi.url_scheme': 'http', '
	HTTP_X_REAL_IP': '140.207.54.73', '
	SERVER_SOFTWARE': 'gevent/1.2 Python/3.5', '
	HTTP_X_LC_DOMAIN': 'mengquapptest', '
	REMOTE_ADDR': '::ffff:10.10.68.29', '
	wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='UTF-8'>, '
	SERVER_PROTOCOL': 'HTTP/1.1', '
	HTTP_CONNECTION': 'close', '
	werkzeug.request': <Request 'http://mengquapptest.leanapp.cn/a/' [POST]>, '
	wsgi.multithread': False, '
	SCRIPT_NAME': '', '
	wsgi.multiprocess': False, '
	wsgi.input': <gevent.pywsgi.Input object at 0x7f81df6a08e8>, '
	wsgi.run_once': False, '
	QUERY_STRING': '', '
	HTTP_X_FORWARDED_PROTO': 'https', '
	GATEWAY_INTERFACE': 'CGI/1.1', '
	REMOTE_PORT': '50488', '
	PATH_INFO': '/a/', '
	HTTP_USER_AGENT': 'Mozilla/4.0', '
	leanengine.request': <Request 'http://mengquapptest.leanapp.cn/a/' [POST]>, '
	SERVER_PORT': '3000', '
	HTTP_PRAGMA': 'no-cache', '
	HTTP_HOST': 'mengquapptest.leanapp.cn', '
	REQUEST_METHOD': 'POST', '
	HTTP_X_AVOSCLOUD_CODE_WEB_HOSTING': '1', '
	HTTP_ACCEPT': '*/*', '
	CONTENT_LENGTH': '785', '
	SERVER_NAME': '::', '
	CONTENT_TYPE': 'text/xml'
}
STDOUT web1 19:57:28
body*20

	<xml>
		<appid><![CDATA[wxed3467f6c5d18070]]></appid>

		<bank_type><![CDATA[CFT]]></bank_type>

		<cash_fee><![CDATA[1]]></cash_fee>

		<fee_type><![CDATA[CNY]]></fee_type>

		<is_subscribe><![CDATA[N]]></is_subscribe>

		<mch_id><![CDATA[1489365792]]></mch_id>

		<nonce_str><![CDATA[BybsX83fIcDTjLdP8VPVE5ChcCzAdOi7]]></nonce_str>

		<openid><![CDATA[oItwWvzTNYiM2WVZydbj5S2KJG7g]]></openid>

		<out_trade_no><![CDATA[5c0e547e1579a3005fd4e3bcx1]]></out_trade_no>

		<result_code><![CDATA[SUCCESS]]></result_code>

		<return_code><![CDATA[SUCCESS]]></return_code>

		<sign><![CDATA[8BC155FE40142A44D0C495AB6B4B3D55]]></sign>

		<time_end><![CDATA[20181210195655]]></time_end>

		<total_fee>1</total_fee>

		<trade_type><![CDATA[APP]]></trade_type>

		<transaction_id><![CDATA[4200000214201812101813178945]]></transaction_id>
	</xml>
'''