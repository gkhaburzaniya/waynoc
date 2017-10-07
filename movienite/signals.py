from datetime import date

from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver

from .models import Movie, Person


@receiver(m2m_changed, sender=Movie.attendees.through)
def movie_changed(sender, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        _recalculate_scores()


@receiver(post_delete, sender=Movie)
def movie_deleted(sender, **kwargs):
    _recalculate_scores()


def _recalculate_scores():
    for person in Person.objects.all():
        if person.movies_attended.count() == 0:
            continue
        person.score = -100 * person.movies_picked.count()
        movies_attended = person.movies_attended.order_by('-date')
        person.score -= (date.today() - movies_attended[0].date).days

        for movie in movies_attended:
            person.score += 100//movie.attendees.count()

        if person.score < 50 and person.movies_picked.count() == 0:
            person.score = None

        person.save()
