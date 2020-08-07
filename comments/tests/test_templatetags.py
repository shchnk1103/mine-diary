from datetime import timedelta
from django.utils import timezone
from comments.models import Comment
from comments.templatetags.comments_extras import show_comment_form, show_comments
from comments.tests.base import CommentDataTestCase
from django.template import Context, Template
from comments.forms import CommentForm


class CommentExtraTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.context = Context()

    def test_show_comment_form_with_empty_form(self):
        template = Template(
            "{% load comments_extras %}" "{% show_comment_form post %}")
        form = CommentForm()
        context = Context(show_comment_form(self.context, self.post))
        expected_html = template.render(context)
        for field in form:
            label = '<label for="{}">{}：</label>'.format(
                field.id_for_label, field.label)
            self.assertInHTML(label, expected_html)
            self.assertInHTML(str(field), expected_html)

    def test_show_comment_form_with_invalid_bound_form(self):
        template = Template(
            "{% load comments_extras %}" "{% show_comment_form post form %}")
        invalid_data = {
            'email': 'invalid_email'
        }
        form = CommentForm(data=invalid_data)
        self.assertFalse(form.is_valid())

        context = Context(show_comment_form(
            self.context, self.post, form=form))
        expected_html = template.render(context)
        for field in form:
            label = '<label for="{}">{}：</label>'.format(
                field.id_for_label, field.label)
            self.assertInHTML(label, expected_html)
            self.assertInHTML(str(field), expected_html)
            self.assertInHTML(str(field.errors), expected_html)

    def test_show_comments_without_any_comment(self):
        template = Template(
            '{% load comments_extras %}' '{% show_comments post %}')
        context_dict = show_comments(self.context, self.post)
        context_dict['post'] = self.post
        context = Context(context_dict)
        expected_html = template.render(context)
        self.assertInHTML('<h3>评论列表，共 <span>0</span> 条评论</h3>', expected_html)
        self.assertInHTML('暂无评论', expected_html)

    def test_show_comments_with_comments(self):
        comment1 = Comment.objects.create(
            name='tester',
            email='test@test.com',
            text='test',
            post=self.post,
            created_time=timezone.now() - timedelta(days=1),
        )
        comment2 = Comment.objects.create(
            name='tester2',
            email='test2@test.com',
            text='test2',
            post=self.post,
            created_time=timezone.now() - timedelta(days=1),
        )
        template = Template(
            "{% load comments_extras %}" "{% show_comments post %}")
        context_dict = show_comments(self.context, self.post)
        context_dict['post'] = self.post
        context = Context(context_dict)
        expected_html = template.render(context)
        self.assertInHTML('<h3>评论列表，共 <span>2</span> 条评论</h3>', expected_html)
        self.assertInHTML(comment1.name, expected_html)
        self.assertInHTML(comment1.text, expected_html)
        self.assertInHTML(comment2.name, expected_html)
        self.assertInHTML(comment2.text, expected_html)

        self.assertQuerysetEqual(
            context_dict['comment_list'], [repr(comment) for comment in [comment2, comment1]])
