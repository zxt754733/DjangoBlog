# -*- coding: utf-8 -*-
"""
Created on 2018/11/19 14:25
Author  : zxt
File    : urls.py
Software: PyCharm
"""

from django.urls import path
from . import views


urlpatterns = [
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
]
