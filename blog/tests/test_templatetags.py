from datetime import timedelta
from re import template
from django.utils import timezone
from blog.templatetags.blog_extras import show_archives, show_categories, show_recent_posts, show_tags
from django.template import Context, Template
from blog.models import Category, Post, Tag
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models.aggregates import Count


class BlogExtreTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='admin',
            email='admin@example.com',
            password='admin',
        )
        self.categories = Category.objects.create(name='测试')
        self.context = Context()

    def test_show_recent_posts_without_any_posts(self):
        template = Template('{% load blog_extras %}' '{% show_recent_posts %}')
        expected_html = template.render(self.context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">最新文章</h3>', expected_html)
        self.assertInHTML('暂无文章！', expected_html)

    def test_show_recent_posts_with_posts(self):
        post = Post.objects.create(
            title='测试标题',
            body="测试内容",
            categories=self.categories,
            author=self.user,
        )
        context = Context(show_recent_posts(self.context))
        template = Template("{% load blog_extras %}" "{% show_recent_posts %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">最新文章</h3>', expected_html)
        self.assertInHTML(
            '<a href="{}">{}</a>'.format(post.get_absolute_url(), post.title), expected_html)

    def test_show_recent_posts_nums_specified(self):
        post_list = []
        for i in range(7):
            post = Post.objects.create(
                title='测试标题-{}'.format(i),
                body='测试内容',
                categories=self.categories,
                author=self.user,
            )
            post_list.insert(0, post)
        context = Context(show_recent_posts(self.context, 3))
        template = Template("{% load blog_extras %}" "{% show_recent_posts %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">最新文章</h3>', expected_html)
        self.assertInHTML('<a href="{}">{}</a>'.format(
            post_list[0].get_absolute_url(), post_list[0].title), expected_html)
        self.assertInHTML('<a href="{}">{}</a>'.format(
            post_list[1].get_absolute_url(), post_list[1].title), expected_html)
        self.assertInHTML('<a href="{}">{}</a>'.format(
            post_list[2].get_absolute_url(), post_list[2].title), expected_html)

    def test_show_recent_posts_without_any_posts(self):
        context = Context(show_archives(self.context))
        template = Template("{% load blog_extras %}" "{% show_archives %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">归档</h3>', expected_html)
        self.assertInHTML('暂无归档！', expected_html)

    def test_show_archives_with_post(self):
        post1 = Post.objects.create(
            title='测试标题-1',
            body='测试内容',
            categories=self.categories,
            author=self.user,
            created_time=timezone.now()
        )
        post2 = Post.objects.create(
            title='测试标题-2',
            body='测试内容',
            categories=self.categories,
            author=self.user,
            created_time=timezone.now() - timedelta(days=50)
        )
        context = Context(show_archives(self.context))
        template = Template("{% load blog_extras %}" "{% show_archives %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">归档</h3>', expected_html)

        # 1
        created_time = post1.created_time
        url = reverse('blog:archives', kwargs={
                      'year': created_time.year, 'month': created_time.month})
        num_posts = Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth(
            'created_time')).values('year', 'month').order_by('year', 'month').annotate(num_posts=Count('id'))
        frag = '<a href="{}">{} 年 {} 月 <span class="post-count">( {} )</a>'.format(
            url, created_time.year, created_time.month, num_posts[0]['num_posts'])
        self.assertInHTML(frag, expected_html)

        # 2
        created_time = post2.created_time
        url = reverse("blog:archives", kwargs={
                      "year": created_time.year, "month": created_time.month})
        frag = '<a href="{}">{} 年 {} 月 <span class="post-count">( {} )</a>'.format(
            url, created_time.year, created_time.month, num_posts[1]['num_posts'])
        self.assertInHTML(frag, expected_html)

    def test_show_categories_without_any_categories(self):
        self.categories.delete()
        context = Context(show_categories(self.context))
        template = Template("{% load blog_extras %}" "{% show_categories %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">分类</h3>', expected_html)
        self.assertInHTML('暂无分类！', expected_html)

    def test_show_categories_with_categories(self):
        categories_with_posts = Category.objects.create(
            name='有文章的分类')
        Post.objects.create(
            title="测试标题-1",
            body="测试内容",
            categories=categories_with_posts,
            author=self.user,
        )

        another_categories_with_posts = Category.objects.create(
            name='另一个有文章的分类')
        Post.objects.create(
            title="测试标题-2",
            body="测试内容",
            categories=another_categories_with_posts,
            author=self.user,
        )
        context = Context(show_categories(self.context))
        template = Template("{% load blog_extras %}" "{% show_categories %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">分类</h3>', expected_html)

        url = reverse('blog:categories', kwargs={
                      'pk': categories_with_posts.pk})
        num_posts = categories_with_posts.post_set.count()
        frag = '<a href="{}">{} <span class="post-count">( {} )</span></a>'.format(
            url, categories_with_posts.name, num_posts)
        self.assertInHTML(frag, expected_html)

        url = reverse('blog:categories', kwargs={
                      'pk': another_categories_with_posts.pk})
        num_posts = another_categories_with_posts.post_set.count()
        frag = '<a href="{}">{} <span class="post-count">( {} )</span></a>'.format(
            url, another_categories_with_posts.name, num_posts)
        self.assertInHTML(frag, expected_html)

    def test_show_tags_without_any_tags(self):
        context = Context(show_tags(self.context))
        template = Template("{% load blog_extras %}" "{% show_tags %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">标签云</h3>', expected_html)
        self.assertInHTML('暂无标签！', expected_html)

    def test_show_tags_with_tags(self):
        tag1 = Tag.objects.create(name="测试1")
        tag2 = Tag.objects.create(name="测试2")
        tag3 = Tag.objects.create(name="测试3")
        post_tag2 = Post.objects.create(
            title='测试标题',
            body="测试内容",
            categories=self.categories,
            author=self.user,
        )
        post_tag2.tags.add(tag2)
        post_tag2.save()

        another_post_tag2 = Post.objects.create(
            title='测试标题',
            body="测试内容",
            categories=self.categories,
            author=self.user,
        )
        another_post_tag2.tags.add(tag2)
        another_post_tag2.save()

        post_tag3 = Post.objects.create(
            title='测试标题',
            body="测试内容",
            categories=self.categories,
            author=self.user,
        )
        post_tag3.tags.add(tag3)
        post_tag3.save()

        context = Context(show_tags(self.context))
        template = Template("{% load blog_extras %}" "{% show_tags %}")
        expected_html = template.render(context)
        self.assertInHTML(
            '<h3 class="widget-title entry-title">标签云</h3>', expected_html)

        url_tag2 = reverse('blog:tags', kwargs={'pk': tag2.pk})
        num_posts_tag2 = tag2.post_set.count()
        frag = '<a href="{}">{} <span class="post-count">( {} )</a>'.format(
            url_tag2, tag2.name, num_posts_tag2)
        self.assertInHTML(frag, expected_html)

        url_tag3 = reverse('blog:tags', kwargs={'pk': tag3.pk})
        num_posts_tag3 = tag3.post_set.count()
        frag = '<a href="{}">{} <span class="post-count">( {} )</a>'.format(
            url_tag3, tag3.name, num_posts_tag3)
        self.assertInHTML(frag, expected_html)
