# -*-coding:utf-8-*-

import json
import logging
import threading

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import reverse

worker_local = threading.local()  # 记录request数据


class RequestLogMiddleware(MiddlewareMixin):
    """
    功能说明：request日志中间件
    ----------------------------------------
    修改人        修改时间        修改原因
    ----------------------------------------
    ld         2020-09-23        new
    ----------------------------------------
    """

    # 忽略入参的url别名元组
    IGNORE_DATA_URL_NAMES = ()

    @staticmethod
    def handle_request_data(request):
        """获取请求数据

        :param request: obj
        :return: url参数, 请求体数据
        """
        req_url_params = {}
        for k, v in dict(request.GET).items():
            if isinstance(v, list) and len(v) == 1:
                req_url_params[k] = v[0]
            else:
                req_url_params[k] = v
        try:
            # print(request.body)
            # print(request.content_type)
            req_body = json.loads(request.body)
        except (json.decoder.JSONDecodeError, Exception) as e:
            req_body = {}
        return req_url_params, req_body

    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        worker_local.ip = ip
        worker_local.path = request.get_full_path()
        worker_local.method = request.method
        ignore_data_urls = iter(reverse(name) for name in self.IGNORE_DATA_URL_NAMES)
        if worker_local.path in ignore_data_urls:
            return None
        url_params, body = self.handle_request_data(request=request)
        worker_local.req_data = dict(url_params=url_params, body=body)


class RequestLogFilter(logging.Filter):
    """
    功能说明：request日志过滤器
    ----------------------------------------
    修改人        修改时间        修改原因
    ----------------------------------------
    ld         2020-09-23        new
    ----------------------------------------
    """

    def filter(self, record):
        record.ip = getattr(worker_local, 'ip', '')
        record.path = getattr(worker_local, 'path', '')
        record.method = getattr(worker_local, 'method', '')
        record.req_data = json.dumps(getattr(worker_local, 'req_data', {}))
        return True
