from datetime import date

from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(default=0, editable=False)  # Score is calculated in signals.py

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(default=date.today)
    picker = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, related_name='picked')
    attendees = models.ManyToManyField(Person, related_name='attended')

    def __str__(self):
        return f'{self.movie}: {self.date}'
