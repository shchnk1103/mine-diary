from datetime import timedelta
from django.utils import timezone
from blog.models import Category, Post, Tag
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog.feeds import AllPostsRssFeed


class BlogDataTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin',
        )

        self.category1 = Category.objects.create(name='分类一')
        self.category2 = Category.objects.create(name='分类二')

        self.tags1 = Tag.objects.create(name='标签一')
        self.tags2 = Tag.objects.create(name='标签二')

        self.post1 = Post.objects.create(
            title='文章一',
            body='内容一',
            categories=self.category1,
            author=self.user,
        )
        self.post1.tags.add(self.tags1)
        self.post1.save()

        self.post2 = Post.objects.create(
            title='文章二',
            body='内容二',
            categories=self.category2,
            author=self.user,
            created_time=timezone.now() - timedelta(days=100)
        )


class CategoriesViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url1 = reverse('blog:categories', kwargs={
                            'pk': self.category1.pk})
        self.url2 = reverse('blog:categories', kwargs={
                            'pk': self.category2.pk})

    def test_visit_a_nonexistent_category(self):
        url = reverse('blog:categories', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog:index')
        self.assertContains(response, text='暂时还没有发布的文章！')

    def test_with_posts(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog:index')
        self.assertContains(response, text=self.post1.title)
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_queryset = self.category1.post_set.all().order_by('-created_time')
        self.assertQuerysetEqual(
            response.context['post_list'], [repr(p) for p in expected_queryset])


class TagsViewsTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url1 = reverse('blog:tags', kwargs={'pk': self.tags1.pk})
        self.url2 = reverse('blog:tags', kwargs={'pk': self.tags2.pk})

    def test_visit_a_nonexistent_tag(self):
        url = reverse('blog:tags', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog:index')
        self.assertContains(response, text='暂时还没有发布的文章！')

    def test_with_posts(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.post1.title)
        self.assertTemplateUsed('blog:index')
        self.assertIn('post_list', response.context)
        self.assertIn('is_paginated', response.context)
        self.assertIn('page_obj', response.context)
        self.assertEqual(response.context['post_list'].count(), 1)
        expected_queryset = self.tags1.post_set.all().order_by('-created_time')
        self.assertQuerysetEqual(
            response.context['post_list'], [repr(p) for p in expected_queryset])


class IndexViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:index')

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog:index')
        self.assertContains(response, text='暂时还没有发布的文章！')

    def test_with_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=self.post1.title)
        self.assertContains(response, text=self.post2.title)
        self.assertIn("post_list", response.context)
        self.assertIn("is_paginated", response.context)
        self.assertIn("page_obj", response.context)
        expected_queryset = Post.objects.all().order_by('-created_time')
        self.assertQuerysetEqual(
            response.context['post_list'], [repr(p) for p in expected_queryset])


class ArchivesViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('blog:archives', kwargs={
                           'year': self.post1.created_time.year,
                           'month': self.post1.created_time.month,
                           })

    def test_without_any_post(self):
        Post.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog:index')
        self.assertContains(response, text='暂时还没有发布的文章！')

    def test_with_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("blog/index.html")
        self.assertContains(response, self.post1.title)
        self.assertIn("post_list", response.context)
        self.assertIn("is_paginated", response.context)
        self.assertIn("page_obj", response.context)

        self.assertEqual(response.context["post_list"].count(), 1)
        now = timezone.now()
        expected_queryset = Post.objects.filter(
            created_time__year=now.year, created_time__month=now.month
        )
        self.assertQuerysetEqual(
            response.context["post_list"], [repr(p) for p in expected_queryset]
        )


class PostDetailViewTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.md_post = Post.objects.create(
            title='Markdown 测试标题',
            body='# 标题',
            categories=self.category1,
            author=self.user,
        )
        self.url = reverse('blog:detail', kwargs={'pk': self.md_post.pk})

    def test_good_views(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertIn('post', response.context)
        self.assertContains(response, text=self.md_post.title)

    def test_visit_a_nonexistent_post(self):
        url = reverse('blog:detail', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_increase_views(self):
        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.views, 1)

        self.client.get(self.url)
        self.md_post.refresh_from_db()
        self.assertEqual(self.md_post.views, 2)

    def test_markdownify_post_body_and_set_toc(self):
        response = self.client.get(self.url)
        self.assertContains(response, '文章目录')
        self.assertContains(response, self.md_post.title)

        post_template = response.context['post']
        self.assertHTMLEqual(post_template.body_html, "<h1 id='_1'>标题</h1>")
        self.assertHTMLEqual(post_template.toc, '<li><a href="#_1">标题</li>')


class AdminTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('admin:blog_post_add')

    def test_set_author_after_publishing_the_post(self):
        data = {
            'title': '测试标题',
            'body': '测试内容',
            'categories': self.category1.pk,
        }
        self.client.login(username=self.user.username, password='admin')
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        post = Post.objects.all().latest('created_time')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, data.get('title'))
        self.assertEqual(post.categories, self.category1)


class RSSTestCase(BlogDataTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('rss')

    def test_rss_subscription_content(self):
        response = self.client.get(self.url)
        self.assertContains(response, text=AllPostsRssFeed.title)
        self.assertContains(response, text=AllPostsRssFeed.description)
        self.assertContains(response, text=self.post1.title)
        self.assertContains(response, text=self.post2.title)
        self.assertContains(response, text='[%s] %s' % (
            self.post1.categories, self.post1.title))
        self.assertContains(response, text='[%s] %s' % (
            self.post2.categories, self.post2.title))
        self.assertContains(response, text=self.post1.body)
        self.assertContains(response, text=self.post2.body)
