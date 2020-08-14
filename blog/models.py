import re
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from markdown.extensions.toc import TocExtension, slugify
from django.utils.functional import cached_property


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}


# 分类
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


# 文章
class Post(models.Model):
    # 作者
    author = models.ForeignKey(
        User, verbose_name='作者', on_delete=models.CASCADE)
    # 标题
    title = models.CharField('标题', max_length=100)
    # 正文
    body = models.TextField('正文')
    # 创建时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    # 修改时间
    modified_time = models.DateTimeField('修改时间')
    # 摘要
    excerpt = models.CharField('摘要', max_length=100, blank=True)
    # 分类
    categories = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)
    # 浏览量
    views = models.PositiveIntegerField('浏览量', default=0, editable=False)
    # 点赞数
    likes = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:50]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

    @property
    def toc(self):
        return self.rich_content.get('toc', '')

    @property
    def body_html(self):
        return self.rich_content.get('content', '')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
