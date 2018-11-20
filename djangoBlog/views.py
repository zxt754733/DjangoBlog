# -*- coding: utf-8 -*-
"""
Created on 2018/8/16 15:38
Author  : zxt
File    : views.py
Software: PyCharm
"""

from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from django.http import JsonResponse
from read_statistics.utils import get_week_read_data, get_today_hot_data
from read_statistics.utils import get_yesterday_hot_data, get_week_hot_data
from blog.models import Blog
from .forms import LoginForm, RegForm


context = {}


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_week_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    week_hot_data = cache.get('week_hot_data')
    if week_hot_data is None:
        week_hot_data = get_week_hot_data()
        cache.set('week_hot_data', week_hot_data, 3600)

    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['week_hot_data'] = week_hot_data
    return render(request, 'home.html', context)
