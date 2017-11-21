from datetime import date

from django.db import models
from django.dispatch import receiver
from django.urls import reverse_lazy


class Person(models.Model):
    name = models.CharField(max_length=255, unique=True)
    score = models.IntegerField(null=True, editable=False)

    def update_score(self):
        movies_attended = self.movies_attended.order_by('-id')
        try:
            self.score = movies_attended[0].id
        except IndexError:
            return
        self.score += movies_attended.count()
        self.score -= 100 * self.movies_picked.count()
        for movie in movies_attended:
            self.score += 100//movie.attendees.count()
        self.save()

    def get_absolute_url(self):
        return reverse_lazy('movienite:person_detail', args=[self.id])

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


@receiver(models.signals.m2m_changed, sender=Movie.attendees.through)
def movie_save(instance, action, pk_set, **_):
    if action in ['post_add', 'post_remove']:
        for attendee in instance.attendees.all():
            attendee.update_score()
    if action == 'post_remove':
        for pk in pk_set:
            Person.objects.get(pk=pk).update_score()
