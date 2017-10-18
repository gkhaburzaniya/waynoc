from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Person, Movie
from .forms import MovieForm


class MovieCreateView(CreateView):
    model = Movie
    form_class = MovieForm
    success_url = reverse_lazy('movienite:movie_list')

    def form_valid(self, form, *args, **kwargs):
        form_data = form.cleaned_data
        cleaned_names = (
            x.strip()
            for x
            in form_data['other_attendees'].split(',')
            if x
        )
        for name in cleaned_names:
            attendee = Person.objects.create(name=name.strip())
            form_data['attendees'] |= Person.objects.filter(id=attendee.id)
        response = super().form_valid(form, *args, **kwargs)
        for person in form_data['attendees']:
            _update_score(person)
        return response


def _update_score(person):
    movies_attended = person.movies_attended.order_by('-id')
    person.score = movies_attended[0].id
    person.score += movies_attended.count()
    person.score -= 100 * person.movies_picked.count()

    for movie in movies_attended:
        person.score += 100//movie.attendees.count()

    person.save()
