from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Movie
from .forms import MovieForm


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movienite:movie_list')

    def form_valid(self, form, *args, **kwargs):
        response = super().form_valid(form, *args, **kwargs)
        for person in form.cleaned_data['attendees']:
            _update_score(person)
        return response


class MovieUpdateView(UpdateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movienite:movie_list')

    def form_valid(self, form, *args, **kwargs):
        # original_attendees = Movie.objects.get(id=self.kwargs.get('pk')).attendees.all()
        response = super().form_valid(form, *args, **kwargs)
        for person in form.cleaned_data['attendees']:
            _update_score(person)
        # for person in original_attendees:
        #     _update_score(person)
        return response


def _update_score(person):
    movies_attended = person.movies_attended.order_by('-id')
    person.score = movies_attended[0].id
    person.score += movies_attended.count()
    person.score -= 100 * person.movies_picked.count()
    for movie in movies_attended:
        person.score += 100//movie.attendees.count()
    person.save()
