# coding: utf-8
# author: zpta

from django.urls import path, include


urlpatterns = [
    path("swagger/", include("apps.swagger_using.urls")),  # swagger
]
