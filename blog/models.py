from django.db.models import Model, CharField, TextField, DateTimeField
from django.utils import timezone


class Post(Model):
    title = CharField(max_length=255)
    text = TextField()
    date = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
