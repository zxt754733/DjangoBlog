# -*- coding: utf-8 -*-
"""
Created on 2018/11/17 16:48
Author  : zxt
File    : urls.py
Software: PyCharm
"""

from django.urls import path
from . import views


urlpatterns = [
    path('like_change', views.like_change, name='like_change'),
]
