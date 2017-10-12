from datetime import date

from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Person, Movie
from .forms import MovieForm


class CreateMovieView(CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movienite:movie_list')

    def form_valid(self, *args, **kwargs):
        response = super().form_valid(*args, **kwargs)
        _recalculate_scores()
        return response


def _recalculate_scores():
    for person in Person.objects.all():
        movies_attended = list(person.movies_attended.order_by('-date'))
        try:
            person.score = -(date.today() - movies_attended[0].date).days
            person.score += (date.today() - movies_attended[-1].date).days//30
        except IndexError:
            continue
        person.score -= 100 * person.movies_picked.count()

        for movie in movies_attended:
            person.score += 100//movie.attendees.count()

        if person.score < 50 and person.movies_picked.count() == 0:
            person.score = None

        person.save()
