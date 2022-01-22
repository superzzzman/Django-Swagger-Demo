# coding: utf-8

from libs.utils.common import PDecimal
from django.db.models.fields import DecimalField
from django.utils.translation import gettext_lazy as _


class PDecimalField(DecimalField):
    """
    功能说明：自定义Decimal类，
    使从DB获取的值支持与 float, int, number-like str, decimal 直接加减乘除
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld       2021-02-08      new
    -------------------------------
    """
    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must can trans to a decimal number."),
    }
    description = _("PDecimal number")

    def from_db_value(self, value, expression, connection):
        """数据库返回的值转换为Python对象"""
        if value is None:
            return value
        return PDecimal(value, n=self.decimal_places)
