from django.test import TestCase

from .models import Post


class BlogTest(TestCase):

    def test_post_str(self):
        hackers = Post.objects.create(title='First')
        self.assertEqual(str(hackers), 'First')
