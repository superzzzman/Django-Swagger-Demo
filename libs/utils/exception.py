# coding: utf-8


class BaseError(Exception):
    """基础异常类"""
    pass


class ClsType(type):
    """
    功能说明：动态创建类
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-01-04      new
    --------------------------------
    """
    __slots__ = ()

    def __call__(cls, *args, **kwargs):
        return super(ClsType, cls).__call__(*args, **kwargs)

    def __new__(mcs, name, bases=(BaseError, ), code_=500, msg_='服务异常，请稍后重试', desc_='服务器异常'):
        """创建类
        :param name: str: 类名
        :param bases: tuple: 基类元组
        :param code_: int: 错误码
        :param msg_: str: 错误信息（用户展示）
        :param desc_: str: 错误描述（开发人员展示）
        """
        def cls_init(self, code=None, msg=None, error=None, ex_error=None, desc=None, ex_desc=None, **kwargs):
            """init函数
            常用： error_msg_ext, error_desc_ext
            :param self:
            :param code: int: 错误码
            :param msg: str: 错误信息（用户展示）
            :param desc: str: 错误描述（开发人员展示）
            :param error: str: 错误信息（英文，开发人员展示）
            :param ex_error: str: 错误信息扩展（英文，开发人员展示，常用于字段名）
            :param desc: str: 错误描述（开发人员展示）
            :param ex_desc: str: 错误描述扩展（中文，开发人员展示）
            """
            self.code = code or code_  # 错误码
            self.message = msg or msg_  # 错误信息（用户展示）
            self.error = error or name  # 错误信息（英文，开发人员展示）
            self.ex_error = ex_error  # 错误信息扩展（英文，开发人员展示）
            self.desc = desc or desc_  # 错误描述（中文，开发人员展示）
            self.ex_desc = ex_desc  # 错误描述扩展（中文，开发人员展示）
        slots = ('code', 'msg', 'error', 'ex_error', 'desc', 'ex_desc')
        return super(ClsType, mcs).__new__(mcs, name, bases, {'__init__': cls_init, '__slots__': slots})

    def __init__(cls, name, bases=(BaseError, ), **kwargs):
        super(ClsType, cls).__init__((name, bases, {}))


"""通用"""

# 未找到页面
PageNotFound = ClsType('PageNotFound', code_='404', desc_='未找到页面')

# 未知异常，服务器异常
ServerError = ClsType('ServerError', code_='500', desc_='服务器异常', msg_='服务异常，请稍后重试')


"""参数相关"""

'''参数相关，1000起始'''
# 格式错误（入参为非json）
UnsupportedMediaType = ClsType('UnsupportedMediaType', code_='1001', desc_='不支持的媒体类型')  # 入参为非json

# 参数类型错误
InvalidParamType = ClsType('InvalidParamType', code_='1002', desc_='错误的参数类型')

# 参数范围错误（参数相关错误都是400）
InvalidParamRange = ClsType('InvalidParamRange', code_='1003', desc_='错误的参数范围')

# 缺失必传参数（参数相关错误都是400）
MissingParameters = ClsType('MissingParameters', code_='1004', desc_='参数缺失')

# 空白符错误
InvalidBlankParam = ClsType('InvalidBlankParam', code_='1005', desc_='参数中含有空白符')

# 正则匹配错误
ParamRegexpMatchFailed = ClsType('ParamRegexpMatchFailed', code_='1006', desc_='参数正则匹配失败')

'''文件相关，1100起始'''
# 文件错误
InvalidFile = ClsType('InvalidFile', code_='1100', desc_='无效文件')

# 无文件名
MissingFileName = ClsType('MissingFileName', code_='1101', desc_='缺失文件名')

# 不支持的文件格式
UnsupportedFileType = ClsType('UnsupportedFileType', code_='1102', desc_='不支持的文件格式', msg_='不支持的文件格式')


"""权限，3000起"""
# 权限拒绝
PermissionDenied = ClsType('PermissionDenied', code_='3000', desc_='权限被拒绝')


"""session，4000起"""
# Session认证异常
SessionExpiredOrNotExist = ClsType('SessionExpiredOrNotExist', code_='4000', desc_='session过期或不存在')
TokenExpiredOrNotExist = ClsType('TokenExpiredOrNotExist', code_='4001', desc_='token过期或不存在')


"""频率相关, 5000起"""
ThrottleDenied = ClsType('ThrottleDenied', code_='5000', desc_='频率限制')


"""请求方式、版本号，6000起"""
# 请求方式异常（get, post等）
MethodNotAllowed = ClsType('MethodNotAllowed', code_='6001', desc_='非法的请求方式')

# 版本号异常
InvalidVersion = ClsType('InvalidVersion', code_='6002', desc_='无效的版本号')

