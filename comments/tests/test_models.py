from comments.tests.base import CommentDataTestCase
from comments.models import Comment


class CommentModelTestCase(CommentDataTestCase):
    def setUp(self):
        super().setUp()
        self.comment = Comment.objects.create(
            name=self.user,
            email=self.user,
            text='test1',
            post=self.post,
        )

    def test_str_representation(self):
        self.assertEqual(self.comment.__str__(), 'test1')
