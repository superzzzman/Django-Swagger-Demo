# -*-coding:utf-8-*-

from rest_framework.versioning import BaseVersioning
from libs.utils.exception import InvalidVersion


class ReqHeaderVersioning(BaseVersioning):
    """
    功能说明：获取请求头的版本号
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2020-09-07      new
    -------------------------------
    """
    def determine_version(self, request, *args, **kwargs):
        """确定版本"""
        version = request.headers.get(self.version_param, self.default_version)
        if not self.is_allowed_version(version):
            raise InvalidVersion
        return version

    def is_allowed_version(self, version):
        return super(ReqHeaderVersioning, self).is_allowed_version(version)
