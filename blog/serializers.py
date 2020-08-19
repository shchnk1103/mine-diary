from rest_framework import serializers
from rest_framework import fields
from blog.models import Category, Post
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class PostListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    author = UserSerializer()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'created_time',
            'excerpt',
            'author',
            'categories',
            'views',
        ]


class PostRetrieveSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    author = UserSerializer()
    toc = serializers.CharField()
    body_html = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'body',
            'created_time',
            'modified_time',
            'excerpt',
            'views',
            'categories',
            'author',
            'toc',
            'body_html',
        ]
