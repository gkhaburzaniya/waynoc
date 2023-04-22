from datetime import date

from django.db.models import (Model, CharField, IntegerField, DateField,
                              ForeignKey, SET_NULL, ManyToManyField, signals)
from django.dispatch import receiver
from django.urls import reverse


class Person(Model):
    name = CharField(max_length=255, unique=True)
    score = IntegerField(null=True, editable=False)

    def update_score(self):
        movies_attended = self.movies_attended.all()
        try:
            self.score = movies_attended.latest().id * 2
        except Movie.DoesNotExist:
            self.delete()
            return
        self.score += movies_attended.count()
        self.score -= 100 * self.movies_picked.count()
        for movie in movies_attended:
            self.score += 100//movie.attendees.count()
        self.save()

    def get_absolute_url(self):
        return reverse('movienite:person_detail', args=[self.id])

    class Meta:
        ordering = ['-score', 'name']

    def __str__(self):
        return self.name


class Movie(Model):
    title = CharField(max_length=255)
    date = DateField(default=date.today)
    picker = ForeignKey(Person, on_delete=SET_NULL, null=True,
                        related_name='movies_picked')
    attendees = ManyToManyField(Person, related_name='movies_attended')

    def delete(self, *args, **kwargs):
        attendees = list(self.attendees.all())
        retval = super().delete(*args, **kwargs)
        for attendee in attendees:
            attendee.update_score()
        return retval

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'

    def __str__(self):
        return f'{self.title}: {self.date}'


@receiver(signals.m2m_changed, sender=Movie.attendees.through)
def movie_save(instance, action, pk_set, **_):
    if action in ['post_add', 'post_remove']:
        for attendee in instance.attendees.all():
            attendee.update_score()
    if action == 'post_remove':
        for pk in pk_set:
            Person.objects.get(pk=pk).update_score()
