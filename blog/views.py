from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import markdown
from markdown import extensions
from .models import Post


def index(request):
    post_list = Post.objects.order_by('-created_time')
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    context = {'post': post}
    return render(request, 'blog/detail.html', context)
