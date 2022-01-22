# -*-coding:utf-8-*-

import datetime
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from collections.abc import ValuesView, KeysView
from libs.utils.common import PDecimal


def to_unix_timestamp(dt: datetime.datetime) -> float:
    """datetime转时间戳"""
    try:
        secs = dt.timestamp()
    except OSError:  # 兼容windows环境
        import calendar
        secs = calendar.timegm((dt + datetime.timedelta(hours=-8)).timetuple())  # 只能保留到整数位
    return secs


class JsonEncoder(DjangoJSONEncoder):
    """
    功能说明：序列化方法
    --------------------------------
    修改人        修改时间        修改原因
    --------------------------------
    ld        2020-09-07        new
    ld        2020-09-10        add QuerySet
    ld        2020-02-20        日期类型兼容windows系统
    --------------------------------
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):  # datetime类型
            # return o.isoformat(sep=' ')
            return to_unix_timestamp(o)  # 时间戳
        elif isinstance(o, datetime.date):  # date类型
            o = datetime.datetime(o.year, o.month, o.day)
            return to_unix_timestamp(o)
        elif isinstance(o, PDecimal):  # PDecimal
            return str(o)
            # return float(o)  # 浮点数，不安全
        elif isinstance(o, QuerySet):  # Django QS
            return list(o)
        elif isinstance(o, set):  # 集合
            return list(o)
        elif isinstance(o, (KeysView, ValuesView)):  # dict_keys, dict_values
            return list(o)
        else:
            return super(JsonEncoder, self).default(o)


def ajax_ok(data=None):
    dic = {
        'code': '0',  # 错误码
        'response': 'ok',  # 信息
        'data': data if data is not None else {},  # 数据
        'desc': '成功'  # 描述
    }
    return JsonResponse(data=dic, encoder=JsonEncoder)


def ajax_fail(code='500', error='ServerError', desc='服务器异常', message='服务异常，请稍后重试', exc=None,
              ece=None, ece_msg=None):
    """

    :param code: int: 错误码
    :param error: str: 错误信息（英文，开发人员展示）
    :param desc: str: 错误描述（中文，开发人员展示）
    :param message: str: 错误信息（用户展示）
    :param exc: obj: 异常
    :param ece: Enum: 枚举
    :param ece_msg: Optional[str]:  错误码自定义message
    :return:
    """
    dic = {
        'code': str(code),
        'response': 'fail',
        'error': error,  # 错误
        'desc': desc,
        'message': message
    }
    if ece:  # 枚举
        code, desc, *msg = ece.value
        message = msg[0] if msg else message
        error = ece.name
        dic['code'], dic['error'], dic['desc'], dic['message'] = str(code), error, desc, ece_msg or message
    elif exc:  # 异常
        dic['code'] = str(exc.code)
        dic['error'] = exc.error if exc.ex_error is None else '%s.%s' % (exc.error, exc.ex_error)
        dic['desc'] = exc.desc if exc.ex_desc is None else '%s（%s）' % (exc.desc, exc.ex_desc)
        dic['message'] = exc.message
    return JsonResponse(data=dic, encoder=JsonEncoder)
