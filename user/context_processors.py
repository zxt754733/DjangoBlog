# -*- coding: utf-8 -*-
"""
Created on 2018/11/19 14:55
Author  : zxt
File    : context_processors.py
Software: PyCharm
"""

from .forms import LoginForm


def login_modal_form(request):
    return {'login_modal_form': LoginForm()}
