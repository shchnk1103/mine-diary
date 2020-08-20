from comments.serializers import CommentSerializer
from blog.filters import PostFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.fields import DateField
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from blog.serializers import PostListSerializer, PostRetrieveSerializer
from blog.forms import PostForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Post
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.models import User
# 引入login装饰器
from django.contrib.auth.decorators import login_required


# 首页
class IndexView(ListView):

    # 要获取的模型是 Post
    model = Post

    # 指定这个视图渲染的模板
    template_name = 'blog/index.html'

    # 获取的模型列表数据保存的变量名
    context_object_name = 'post_list'

    # 指定10篇文章分页
    paginate_by = 8


# 首页
# def index(request):
#     post_list = Post.objects.all()
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


# 详情页
class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):

        HttpResponse = super(PostDetailView, self).get(
            request, *args, **kwargs)

        # 阅读量 + 1
        self.object.increase_views()

        return HttpResponse

    # def get_object(self, queryset=None):

    #     post = super().get_object(queryset=None)

    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)

    #     m = re.search(
    #         r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''

    #     return post


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     # 阅读量 + 1
#     post.increase_views()

#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)

#     # 判断文章目录是否存在
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''

#     context = {'post': post}
#     return render(request, 'blog/detail.html', context)


# 归档
class ArchivesView(IndexView):

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(
            created_time__year=year, created_time__month=month
        )


# def archives(request, year, month):
#     post_list = Post.objects.filter(
#         created_time__year=year, created_time__month=month
#     )
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, 'blog/index.html', context)


# 分类
class CategoryView(IndexView):

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(categories=category)


# def categories(request, pk):
#     category = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(
#         categories=category)
#     context = {'post_list': post_list, }
#     return render(request, 'blog/index.html', context)


# 查找
def search(request):

    # NavBar 中搜索框设置的 name
    q = request.GET.get('q')

    if not q:
        error_message = '请输入关键词'
        messages.add_message(request, messages.ERROR,
                             error_message, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q))
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


# 点赞
class IncreaseLikeView(View):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs.get('id'))
        post.likes += 1
        post.save()
        return HttpResponse('success')


# 写文章
def create_post(request):
    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_article = post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.categories = Category.objects.get(
                id=request.POST['categories'])
            new_article.save()
            return redirect('blog:index')
        else:
            return HttpResponse('表单信息有误，请重新输入～')
    else:
        post_form = PostForm()
        categories = Category.objects.all()
        context = {
            'post_form': post_form,
            'categories': categories,
        }
        return render(request, 'blog/create.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def safe_delete_post(request, id):
    if request.method == "POST":
        article = Post.objects.get(id=id)
        if request.user != article.author:
            messages.add_message(request, messages.ERROR,
                                 '抱歉，你无权修改这篇文章~', extra_tags='danger')
            return redirect('blog:detail', pk=id)
        article.delete()
        return redirect('blog:index')
    else:
        return HttpResponse('仅允许post请求~')


# 更新文章
@login_required(login_url='/userprofile/login/')
def update_post(request, id):
    article = Post.objects.get(id=id)

    if request.user != article.author:
        messages.add_message(request, messages.ERROR,
                             '抱歉，你无权修改这篇文章~', extra_tags='danger')
        return redirect('blog:detail', pk=id)

    if request.method == "POST":
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            article.title = request.POST['title']
            article.categories.id = request.POST['categories']
            article.body = request.POST['body']
            article.save()
            return redirect('blog:detail', pk=id)
        else:
            return HttpResponse('数据不合法，请重新填写～')
    else:
        post_form = PostForm()
        categories = Category.objects.all()
        context = {
            'post_form': post_form,
            'article': article,
            'categories': categories,
        }
        return render(request, 'blog/update.html', context)


# api 首页
class IndexPostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class PostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class_table = {
        'list': PostListSerializer,
        'retrieve': PostRetrieveSerializer,
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_serializer_class(self):
        return self.serializer_class_table.get(
            self.action, super().get_serializer_class()
        )

    @action(
        methods=['GET'],
        detail=False,
        url_path='archive/dates',
        url_name='archive-date'
    )
    def list_archive_dates(self, request, *args, **kwargs):
        dates = Post.objects.dates('created_time', 'month', order='DESC')
        date_field = DateField()
        data = [date_field.to_representation(date) for date in dates]
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=True,
        url_path='comments',
        url_name='comment',
        pagination_class=LimitOffsetPagination,
        serializer_class=CommentSerializer,
    )
    def list_comments(self, request, *args, **kwargs):
        # 根据 URL 传入的参数值（文章 id）获取到博客文章记录
        post = self.get_object()
        # 获取文章下关联的全部评论
        queryset = post.comments_post.all()
        # 对评论列表进行分页，根据 URL 传入的参数获取指定页的评论
        page = self.paginate_queryset(queryset)
        # 序列化评论
        serializer = self.get_serializer(page, many=True)
        # 返回分页后的评论列表
        return self.get_paginated_response(serializer.data)
