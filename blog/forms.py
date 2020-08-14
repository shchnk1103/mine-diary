from django import forms
from blog.models import Post


# 写文章的表单类
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
