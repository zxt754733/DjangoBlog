# -*- coding: utf-8 -*-
"""
Created on 2018/8/10 1:24
Author  : zxt
File    : urls.py
Software: PyCharm
"""

from django.urls import path
from . import views


urlpatterns = [
    path('', views.blogList, name='blog_list'),
    path('<int:blog_pk>', views.blogDetail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blogType, name='blog_type'),
    path('date/<int:year>/<int:month>', views.blogDates, name='blogs_date'),
]

