from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Post


class CommentDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        self.categories = Category.objects.create(
            name='test',
        )
        self.post = Post.objects.create(
            title='Test',
            body='test',
            categories=self.categories,
            author=self.user,
        )
