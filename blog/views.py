import re
from django.shortcuts import get_object_or_404
import markdown
from markdown.extensions.toc import TocExtension, slugify
from .models import Category, Post, Tag
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin


class IndexView(PaginationMixin, ListView):

    # 要获取的模型是 Post
    model = Post

    # 指定这个视图渲染的模板
    template_name = 'blog/index.html'

    # 获取的模型列表数据保存的变量名
    context_object_name = 'post_list'

    # 指定10篇文章分页
    paginate_by = 10


# def index(request):
#     post_list = Post.objects.all()
#     context = {'post_list': post_list}
#     return render(request, 'blog/index.html', context)


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

    def get_object(self, queryset=None):

        post = super().get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)

        m = re.search(
            r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''

        return post


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


class TagsViews(IndexView):

    def get_queryset(self):
        tags = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tags)


# def tags(request, pk):
#     tag = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=tag)
#     context = {'post_list': post_list, }
#     return render(request, 'blog/index.html', context)
