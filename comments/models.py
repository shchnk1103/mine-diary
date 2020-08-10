from django.db import models
from django.utils import timezone
from blog.models import Post
from django.contrib.auth.models import User


class Comment(models.Model):
    name = models.ForeignKey(User, verbose_name='名字',
                             on_delete=models.CASCADE,
                             related_name='comments_name')
    email = models.ForeignKey(User, verbose_name='邮箱',
                              on_delete=models.CASCADE,
                              related_name='comments_email')
    text = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey(Post, verbose_name='文章',
                             on_delete=models.CASCADE,
                             related_name='comments_post')

    def __str__(self) -> str:
        return self.text[:20]

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
