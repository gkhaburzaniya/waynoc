from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.title
