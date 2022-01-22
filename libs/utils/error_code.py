# coding: utf-8

"""错误码相关

demo:

from libs.utils.error_code import ECEnum, ECException

raise ECException(ECEnum.ServerError)
"""


from enum import Enum, unique
from types import SimpleNamespace


def spec_unique(enumeration):
    """Class decorator for enumerations ensuring unique member values."""
    unique(enumeration)
    number_set = set()
    for elem in enumeration:
        first_value = elem.value[0]
        if first_value in number_set:
            raise ValueError('duplicate first value found in %r' % elem)
        number_set.add(first_value)
    del number_set
    return enumeration


@spec_unique
class ErrorCodeEnum(Enum):
    """
    功能说明：错误码枚举类
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-04-20      new
    --------------------------------
    """

    '''元组顺序：
    错误码  开发人员展示 用户展示
    code   desc        message
    '''

    # 服务器相关
    ServerError = ('500', '服务器异常', '服务异常，请稍后重试')
    PageNotFound = ('404', '未找到页面')
    # 参数相关
    UnsupportedMediaType = ('1001', '不支持的媒体类型')
    InvalidParamType = ('1002', '错误的参数类型')
    InvalidParamRange = ('1003', '错误的参数范围')
    MissingParameters = ('1004', '参数缺失')
    InvalidBlankParam = ('1005', '参数中含有空白符')
    ParamRegexpMatchFailed = ('1006', '参数正则匹配失败')
    # 文件相关
    InvalidFile = ('1100', '无效文件')
    MissingFileName = ('1101', '缺失文件名')
    UnsupportedFileType = ('1102', '不支持的文件格式', '不支持的文件格式')
    # 权限
    PermissionDenied = ('3000', '权限被拒绝', '无权限访问')
    # 认证相关
    SessionExpiredOrNotExist = ('4000', 'session过期或不存在')
    TokenExpiredOrNotExist = ('4001', 'token过期或不存在', 'token过期或不存在')
    # 频率限制相关
    ThrottleDenied = ('5000', '频率限制')
    # method and version
    MethodNotAllowed = ('6001', '非法的请求方式')
    InvalidVersion = ('6002', '无效的版本号')
    # 账号
    UserNotExist = ('10000', '用户不存在', '该账号不存在，请前往注册')
    UserLoginForbidden = ('10001', '用户已封禁', '账号已封禁，请联系管理员')
    InvalidAccountOrPassword = ('10002', '用户名或密码错误', '账号或密码输入错误，请重新输入')
    InvalidCaptcha = ('10003', '无效的验证码', '无效的验证码，请重新输入')
    ErrorCaptcha = ('10004', '错误的验证码', '验证码输入错误，请重新输入')
    ExistAccount = ('10005', '已存在的账号', '手机号已注册')
    AccountUnderReview = ('10006', '账号审核中', '账号正在审核中，请稍后登录')
    InconsistentPasswords = ("10007", "密码不一致", "密码不一致")
    CaptchaNotMatchAccount = ("10008", "验证码与账号不匹配", "验证码与账号不匹配")
    # 短信
    SMSServerError = ('30000', '短信服务异常', '短信服务异常，请稍后重试')



class ErrorCodeException(Exception):
    """
    功能说明：错误码异常
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-04-20      new
    --------------------------------
    """

    def __init__(self, ece, message=None):
        """

        :param ece: ErrorCodeEnum: 错误码枚举类
        :param message: Optional[str]: 指定错误信息
        """
        self.ece = ece
        self.message = message


ECEnum = ErrorCodeEnum
ECException = ErrorCodeException
