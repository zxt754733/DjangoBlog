from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
from user.forms import LoginForm


context = {}


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUM)  # 每4篇分页
    page_num = request.GET.get('page', 1)  # 获取页码参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number
    page_range = [(current_page_num + i) for i in range(-2, 3) if paginator.num_pages >= (current_page_num + i) > 0]
    # 获取页码栏的列表，并除去越界页码
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')  # 省略标记
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)  # 首尾页

    """
    # 获取博客分类对应的数量
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
        
    等价于：
    BlogType.objects.annotate(blog_count=Count('blog'))
    """

    # 获取日期归档对应的博客数量
    blog_date_dict = {}
    for blog_date in Blog.objects.dates('created_time', 'month', order='DESC'):
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_date_dict[blog_date] = blog_count

    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 侧边栏博客分类
    context['blogs_date'] = blog_date_dict  # 侧边栏日期归档
    return context


def blogList(request):
    blogs_all_list = Blog.objects.all()
    context_list = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context_list)


def blogType(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    # context['blog_type'] = blog_type
    context['blog_type_name'] = blog_type.type_name
    context_list = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_type.html', context_list)


def blogDates(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    context_list = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blogs_with_date.html', context_list)


def blogDetail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 取出当前博客下一篇
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 取出上一篇
    context['blog'] = blog
    # context['user'] = request.user
    context['comments'] = comments.order_by('-comment_time')
    context['comment_count'] = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count()
    # context['comment_form'] = CommentForm(
    #     initial={
    #         'content_type': blog_content_type,
    #         'object_id': blog_pk,
    #         'reply_comment_id': 0
    #     }
    # )
    # context['login_form'] = LoginForm()
    response = render(request, 'blog/blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # max_age,expires参数不设置时，当浏览器关闭时cookie才失效
    return response
