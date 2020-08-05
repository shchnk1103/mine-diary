from django.contrib import admin
from .models import Comment


class CommentModel(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_time']
    fields = ['name', 'email', 'text', 'post']


admin.site.register(Comment, CommentModel)
