# -*- coding: utf-8 -*-
"""
Created on 2018/10/21 18:53
Author  : zxt
File    : urls.py
Software: PyCharm
"""

from django.urls import path
from . import views


urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
]
