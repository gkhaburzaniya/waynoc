from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Person, Movie
from .forms import MovieForm


class CreateMovieView(CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movienite:movie_list')

    def form_valid(self, form, *args, **kwargs):
        form_data = form.cleaned_data
        if form_data['other_attendees']:
            for name in form_data['other_attendees'].split(','):
                attendee = Person(name=name.strip())
                attendee.save()
                form_data['attendees'] |= Person.objects.filter(id=attendee.id)
        response = super().form_valid(form, *args, **kwargs)
        _recalculate_scores()
        return response


def _recalculate_scores():
    for person in Person.objects.all():
        movies_attended = person.movies_attended.order_by('-date')
        person.score = movies_attended[0].id
        person.score += movies_attended.count()
        person.score -= 100 * person.movies_picked.count()

        for movie in movies_attended:
            person.score += 100//movie.attendees.count()

        person.save()
