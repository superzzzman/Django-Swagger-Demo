# coding: utf-8

"""公共"""

from libs.utils.view import BaseView
from rest_framework_xml.parsers import XMLParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import FormParser


class TextXMLParser(XMLParser):
    media_type = 'text/xml'


class PaymentCallBackView(BaseView):
    """
    功能说明：支付回调视图
    --------------------------------
    修改人      修改时间      修改原因
    --------------------------------
    ld      2021-04-14         添加注释
    -------------------------------
    微信：xml
    阿里: x-www-form-urlencoded
    """

    parser_classes = [TextXMLParser, XMLParser, JSONParser, FormParser]  # 解析器
    authentication_classes = []  # 跳过认证
