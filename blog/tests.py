from django.test import TestCase

from .models import Post


class BlogTest(TestCase):

    def test_post_title(self):
        title = 'Foo'
        Post(title=title, text='bar').save()
        self.assertEqual(str(Post.objects.get(title=title)), title)
