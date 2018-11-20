# -*- coding: utf-8 -*-
"""
Created on 2018/10/17 15:16
Author  : zxt
File    : utils.py
Software: PyCharm
"""

import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from .models import ReadNum, ReadDetail


def read_statistics_once_read(request, obj):
    content_type = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (content_type.model, obj.pk)
    if not request.COOKIES.get(key):  # 使用cookie判断阅读次数
        """
        用get_or_create()函数代替以下代码
        if ReadNum.objects.filter(content_type=content_type, object_id=obj.pk).count():
            # 存在记录直接获取
            readnum = ReadNum.objects.get(content_type=content_type, object_id=obj.pk)
        else:
            # 不存在记录创建记录
            readnum = ReadNum(content_type=content_type, object_id=obj.pk)
        """
        readnum, created = ReadNum.objects.get_or_create(content_type=content_type, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        """
        # 阅读量当天加1判断
        用get_or_create()函数代替以下代码
        if ReadDetail.objects.filter(content_type=content_type, object_id=obj.pk, date=date).count():
            readdetail = ReadDetail.objects.get(content_type=content_type, object_id=obj.pk, date=date)
        else:
            readdetail = ReadDetail(content_type=content_type, object_id=obj.pk, date=date)
        """
        date = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=content_type, object_id=obj.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()

    return key


def get_week_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))  # aggregate，['æɡrɪɡɪt']，聚合
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')  # 倒序
    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')  # 倒序
    return read_details[:7]


"""
以下方法取不到文章title，换用Blog.objects.filter()方法并返回id和title
def get_week_hot_data(content_type):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter(
        content_type=content_type, date__gte=date
    ).values('content_type', 'object_id').annotate(read_num_sum=Sum('read_num')).order_by('-read_num')  # 倒序
    return read_details[:7]
"""


def get_week_hot_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(
        read_details__date__gte=date
    ).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')  # 倒序
    return blogs[:7]
