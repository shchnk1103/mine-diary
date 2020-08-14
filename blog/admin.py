from typing import Any
from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time',
                    'modified_time', 'categories', 'author']
    fields = ['title', 'body', 'excerpt', 'categories']

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
