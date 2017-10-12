from datetime import date

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(null=True, editable=False)

    class Meta:
        ordering = ['-score', 'name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=date.today)
    picker = models.ForeignKey(Person,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='movies_picked')
    attendees = models.ManyToManyField(Person, related_name='movies_attended')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.title}: {self.date}'
