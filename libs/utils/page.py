# -*-coding:utf-8-*-

"""自定义页面"""


from libs.utils.exception import PageNotFound, ServerError
from libs.utils.response import ajax_fail


def page_not_found(request, exception):
    """
    功能说明：404页面
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2020-09-15      new
    -------------------------------
    """
    return ajax_fail(exc=PageNotFound())


def page_server_error(request):
    """
    功能说明：500页面
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2020-09-16      new
    -------------------------------
    """
    return ajax_fail(exc=ServerError())
