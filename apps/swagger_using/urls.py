# coding: utf-8
# author: zpta

from django.urls import path

from apps.swagger_using.views.swagger_using import ReturnJson

urlpatterns = [
    path('api/', ReturnJson.as_view(), name='api'),
]

