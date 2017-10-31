from datetime import date

from django.db import models
from django.urls import reverse_lazy


class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(null=True, editable=False)

    def update_score(self):
        movies_attended = self.movies_attended.order_by('-id')
        self.score = movies_attended[0].id
        self.score += movies_attended.count()
        self.score -= 100 * self.movies_picked.count()
        for movie in movies_attended:
            self.score += 100//movie.attendees.count()
        self.save()

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

    @staticmethod
    def get_absolute_url():
        return reverse_lazy('movienite:movie_list')

    def delete(self, *args, **kwargs):
        attendees = list(self.attendees.all())
        retval = super().delete(*args, **kwargs)
        for attendee in attendees:
            attendee.update_score()
        return retval

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.title}: {self.date}'
