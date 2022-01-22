# coding=utf8
import logging
import time
from django.utils.deprecation import MiddlewareMixin

log = logging.getLogger(__name__)


class SlowLogMiddleware(MiddlewareMixin):
    """
    功能说明：慢日志中间件，原有中间件删除无用功能，仅记录慢日志
    ----------------------------------------
    修改人        修改时间        修改原因
    ----------------------------------------
    ld         2020-09-02        new
    ----------------------------------------
    """
    def __init__(self, *args, **kwargs):
        super(SlowLogMiddleware, self).__init__(*args, **kwargs)
        self.start_time = None

    def _init_time(self):
        """重置时间"""
        self.start_time = None

    def process_view(self,  request, view_func, view_args, view_kwargs):
        self.start_time = time.time()
        return None

    def process_response(self, request, response):
        if self.start_time is None:  # url路由失败
            return response
        use_time = time.time() - self.start_time
        if use_time > 2:  # 操作1秒写入慢执行日志
            log.warning("[use_time:%0.3f]" % use_time)
        else:
            pass
            # 记录所有请求时间，做数据分析使用
            # log.info("[use_time:%0.3f]" % use_time, extra=dict(req=request))
        self._init_time()  # 时间重置
        return response
