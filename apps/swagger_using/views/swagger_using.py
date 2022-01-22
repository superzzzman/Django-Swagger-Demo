# Create your views here.
# -*- coding: utf-8 -*-

from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from rest_framework.schemas import SchemaGenerator, AutoSchema
from rest_framework.schemas.generators import LinkNode, insert_into
from rest_framework.renderers import *
from rest_framework_swagger import renderers
from rest_framework.response import Response

# from rest_framework.schemas import SchemaGenerator
from libs.utils.response import ajax_ok
from libs.utils.view import BaseView


class MySchemaGenerator(SchemaGenerator):

    def get_links(self, request=None):
        # from rest_framework.schemas.generators import LinkNode,
        links = LinkNode()

        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
               continue
            link = view.schema.get_link(path, method, base_url=self.url)
            # 添加下面这一行方便在views编写过程中自定义参数.
            link._fields += self.get_core_fields(view)

            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)

            # from rest_framework.schemas.generators import LinkNode, insert_into
            insert_into(links, keys, link)

        return links

    # 从类中取出我们自定义的参数, 交给swagger 以生成接口文档.
    def get_core_fields(self, view):
        return getattr(view, 'coreapi_fields', ())

def DocParam(name="default", location="query", required=True, description=None, type="string", *args, **kwargs):
    return coreapi.Field(name=name, location=location, required=required, description=description, type=type)

class ReturnJson(BaseView):
    # coreapi_fields = (  #用于swagger doc显示方法必须字符串
    #     DocParam("name", description='test'),
    #     DocParam("nalanxiao", required=False, description='rohero'),
    # )

    # schema = AutoSchema(
    #     manual_fields=[
    #         coreapi.Field(name='code', required=False, location='form', description='', type='string'),
    #     ]
    # )
    def get_v(self, request):
        json_data = {'name': 'post', 'id': 0}
        return ajax_ok(json_data)

    # def post(self, request, *args, **kwargs):
    #     json_data = {'name': 'post', 'id': 0}
    #     # return Response(json_data)
    #     return ajax_ok(json_data)
