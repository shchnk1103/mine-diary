import re
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import markdown
from markdown.extensions.toc import TocExtension, slugify
from .models import Category, Post, Tag


def index(request):
    post_list = Post.objects.order_by('-created_time')
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    # 判断文章目录是否存在
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def archives(request, year, month):
    post_list = Post.objects.filter(
        created_time__year=year, created_time__month=month
    ).order_by('-created_time')
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(
        categories=category).order_by('-created_time')
    context = {'post_list': post_list, }
    return render(request, 'blog/index.html', context)


def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_time')
    context = {'post_list': post_list, }
    return render(request, 'blog/index.html', context)
