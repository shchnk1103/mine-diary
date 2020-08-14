from blog.forms import PostForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Post, Tag
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


# 标签
class TagsViews(IndexView):

    def get_queryset(self):
        tags = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tags)


# def tags(request, pk):
#     tag = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=tag)
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
            return HttpResponse('抱歉，你无权修改这篇文章~')
        article.delete()
        return redirect('blog:index')
    else:
        return HttpResponse('仅允许post请求~')
