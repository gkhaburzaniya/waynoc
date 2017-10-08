from datetime import date

from django.views.generic import CreateView

from .models import Person, Movie


class CreateMovieView(CreateView):
    model = Movie

    def form_valid(self, form):
        response = super().form_valid(form)
        _recalculate_scores()
        return response


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
