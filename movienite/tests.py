from datetime import date

from django.http.request import QueryDict
from django.test import TestCase

from .forms import MovieForm
from .models import Person, Movie


class MovieniteTest(TestCase):

    def test_add_person(self):
        trey = Person.objects.create(name='Trey')
        data = QueryDict(mutable=True)
        data.update({
            'title': 'Hackers',
            'date': '2019-05-16',
            'picker': str(trey.id)})
        data.setlist('attendees', [trey.name, 'George'])
        movie = MovieForm(data=data)
        if movie.is_valid():
            movie.save()
        self.assertTrue(Person.objects.get(name='George'))

    def test_remove_attendee(self):
        trey = Person.objects.create(name='Trey')
        george = Person.objects.create(name='George')
        hackers = Movie.objects.create(id=1, title='Hackers', picker=trey,
                                       date=date.today())
        hackers.attendees.set([trey, george])
        tremors = Movie.objects.create(id=2, title='Tremors', picker=george,
                                       date=date.today())
        tremors.attendees.set([trey, george])
        data = QueryDict(mutable=True)
        data.update({
            'title': hackers.title,
            'date': str(hackers.date),
            'picker': str(hackers.picker_id)})
        data['attendees'] = trey.name
        movie = MovieForm(data=data, instance=hackers)
        trey_score = Person.objects.get(id=trey.id).score
        george_score = Person.objects.get(id=george.id).score
        self.assertEqual(trey_score, george_score)
        if movie.is_valid():
            movie.save()
        self.assertTrue(Person.objects.get(id=trey.id).score > trey_score)
        self.assertTrue(Person.objects.get(id=george.id).score < george_score)
