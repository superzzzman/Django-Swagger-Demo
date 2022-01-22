# coding：utf-8

"""新版视图类"""

from django.core.files import File
from rest_framework.views import APIView
from rest_framework.request import is_form_media_type
from libs.utils.verification import Parameters
from libs.utils.exception import MethodNotAllowed, InvalidVersion


class BaseView(APIView):
    """
    功能说明：封装视图类，越过csrf
    ------------------------------------
    修改人        修改时间        修改原因
    ------------------------------------
    ld         2021-01-04         new
    ld         2021-03-02         逻辑优化
    ld         2021-05-26         代码优化
    ------------------------------------
    """

    def __init__(self, **kwargs):
        self.args = None
        self.kwargs = None
        self.request = None
        self.headers = None
        self.response = None
        self.format_kwarg = None
        super(BaseView, self).__init__(**kwargs)

    def verify(self, request) -> None:
        """参数校验"""
        # verify_v_1_0_0
        method_str = 'verify_v_' + request.version.replace('.', '_')
        if hasattr(self, method_str):
            return getattr(self, method_str)(request)
        return None

    @staticmethod
    def body_params_format(request) -> Parameters:
        """请求体格式化"""
        body_params = Parameters(request.data)
        if is_form_media_type(request.content_type):  # 表单
            for k, v in body_params.items():
                # if isinstance(v, list) and len(v) == 1:
                #     body_params[k] = v[0]
                if isinstance(v, list) and len(v) == 1:
                    if not isinstance(v[0], File):  # 非文件
                        body_params[k] = v[0]
        return body_params

    @staticmethod
    def url_params_format(request) -> Parameters:
        """url参数格式化"""
        url_params = Parameters(request.query_params)
        for k, v in url_params.items():
            if isinstance(v, list) and len(v) == 1:
                url_params[k] = v[0]
        return url_params

    def initial(self, request, *args, **kwargs):
        """
            增加自定义参数
            增加参数校验
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # 新增自定义
        request.body_params = self.body_params_format(request=request)
        request.url_params = self.url_params_format(request=request)

        # 参数校验
        self.verify(request)
        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)

    def _response(self, request, *args, **kwargs):
        """生成response对象
            request.method校验
            version校验
            initial
            response
        """
        version, scheme = self.determine_version(request, *args, **kwargs)
        # 后缀
        suffix = '_v_%s' % (version.replace('.', '_'),)
        method = request.method.lower()
        try:
            # 检验请求方式
            if request.method.lower() not in self.http_method_names:
                raise MethodNotAllowed(ex_error=request.method)
            if request.method != 'OPTIONS':
                # 遍历视图类的方法名
                for func_name in self.__class__.__dict__.keys():
                    if func_name.startswith(method + '_v'):
                        handler = getattr(self, method + suffix, self.http_method_not_allowed)
                        break
                else:
                    raise MethodNotAllowed(ex_error=request.method)
            else:
                handler = getattr(self, method, self.http_method_not_allowed)

            # 检验版本号
            if request.method != 'OPTIONS':
                if not hasattr(self, method + suffix):
                    raise InvalidVersion
            self.initial(request, *args, **kwargs)
            response = handler(request, *args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        return response

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        response = self._response(request, *args, **kwargs)
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
