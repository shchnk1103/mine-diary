from django.db import models
from django.utils import timezone
from blog.models import Post


class Comment(models.Model):
    name = models.CharField('名字', max_length=100)
    email = models.EmailField('邮箱')
    text = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{}: {}'.format(self.name, self.text[:20])

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
