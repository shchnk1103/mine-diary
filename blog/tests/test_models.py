from blog.models import Category, Post, Tag
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class CategoriesModelTestCase(TestCase):
    def setUp(self):
        self.categories = Category.objects.create(name='test')

    def test_str_representation(self):
        self.assertEqual(self.categories.__str__(), self.categories.name)


class TagsModelTestCase(TestCase):
    def setUp(self):
        self.tags = Tag.objects.create(name='test')

    def test_str_representation(self):
        self.assertEqual(self.tags.__str__(), self.tags.name)


class PostModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
        categories = Category.objects.create(name='测试')
        self.post = Post.objects.create(
            title='测试标题',
            body='测试内容',
            categories=categories,
            author=user,
        )

    def test_str_representation(self):
        self.assertEqual(self.post.__str__(), self.post.title)

    def test_auto_populate_modified_time(self):
        self.assertIsNotNone(self.post.modified_time)

        old_post_modified_time = self.post.modified_time
        self.post.body = 'something brand new'
        self.post.save()
        self.post.refresh_from_db()
        self.assertTrue(self.post.modified_time > old_post_modified_time)

    def test_auto_populate_excerpt(self):
        self.assertIsNotNone(self.post.excerpt)
        self.assertTrue(0 < len(self.post.excerpt) < 100)

    def test_get_absolute_url(self):
        expected_url = reverse('blog:detail', kwargs={'pk': self.post.pk})
        self.assertEqual(self.post.get_absolute_url(), expected_url)

    def test_increase_views(self):
        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

        self.post.increase_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 2)
