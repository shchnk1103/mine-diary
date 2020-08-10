from comments.models import Comment
from comments.tests.base import CommentDataTestCase
from django.urls import reverse


class CommentViewTestCase(CommentDataTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('comments:comment', kwargs={
                           'post_pk': self.post.pk})

    # def test_comment_a_nonexistent_post(self):
    #     url = reverse('comments:comment', kwargs={'post_pk': 100})
    #     response = self.client.post(url, {})
    #     self.assertEqual(response.status_code, 404)

    # def test_invalid_comment_data(self):
    #     invalid_data = {
    #         'email': 'invalid_email'
    #     }
    #     response = self.client.post(self.url, invalid_data)
    #     self.assertTemplateUsed(response, 'comments/preview.html')
    #     self.assertIn('post', response.context)
    #     self.assertIn('form', response.context)
    #     form = response.context['form']
    #     for field_name, errors in form.errors.items():
    #         for error in errors:
    #             self.assertContains(response, error)
    #     self.assertContains(response, text='评论失败，请修改表单以后重试～')

    # def test_valid_comment_data(self):
    #     valid_data = {
    #         'name': 'tester',
    #         'email': 'tester@test.com',
    #         'text': 'test',
    #     }
    #     response = self.client.post(self.url, valid_data, follow=True)
    #     self.assertRedirects(response, self.post.get_absolute_url())
    #     self.assertContains(response, text='评论成功！')
    #     self.assertEqual(Comment.objects.count(), 1)
    #     comment = Comment.objects.first()
    #     self.assertEqual(comment.name, valid_data['name'])
    #     self.assertEqual(comment.email, valid_data['email'])
    #     self.assertEqual(comment.text, valid_data['text'])
