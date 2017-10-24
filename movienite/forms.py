from django import forms

from .models import Movie, Person


class MovieForm(forms.ModelForm):
    picker = forms.models.ModelChoiceField(Person.objects.all(), empty_label=None)

    def clean(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        response = super().save(*args, **kwargs)
        for person in self.cleaned_data['attendees']:
            _update_score(person)
        return response

    class Meta:
        model = Movie
        fields = ['title', 'date', 'picker', 'attendees']


def _update_score(person):
    movies_attended = person.movies_attended.order_by('-id')
    person.score = movies_attended[0].id
    person.score += movies_attended.count()
    person.score -= 100 * person.movies_picked.count()
    for movie in movies_attended:
        person.score += 100//movie.attendees.count()
    person.save()
