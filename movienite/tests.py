from datetime import date

from django.http.request import QueryDict
from django.test import TestCase

from .forms import MovieForm
from .models import Person, Movie


class MovieniteTest(TestCase):

    def test_delete_persons_last_movie(self):
        trey = Person.objects.create(name='Trey')
        george = Person.objects.create(name='George')
        movie = Movie.objects.create(title='Hackers', picker=trey)
        movie.attendees.set([trey, george])
        movie.delete()
        self.assertEqual(len(Person.objects.all()), 0)

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
        hackers = Movie.objects.create(title='Hackers', picker=trey)
        hackers.attendees.set([trey, george])
        tremors = Movie.objects.create(title='Tremors', picker=george)
        tremors.attendees.set([trey, george])
        data = QueryDict(mutable=True)
        data.update({
            'title': hackers.title,
            'date': str(hackers.date),
            'picker': str(hackers.picker_id)})
        data['attendees'] = trey.name
        trey_score = Person.objects.get(id=trey.id).score
        george_score = Person.objects.get(id=george.id).score
        self.assertEqual(trey_score, george_score)

        movie = MovieForm(data=data, instance=hackers)
        if movie.is_valid():
            movie.save()
        self.assertTrue(Person.objects.get(id=trey.id).score > trey_score)
        self.assertTrue(Person.objects.get(id=george.id).score < george_score)
