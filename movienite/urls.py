from dal.autocomplete import Select2QuerySetView
from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from .models import Person, Movie
from .views import MovieCreateView, MovieUpdateView

app_name = 'movienite'
urlpatterns = [
    url(
        r'^$',
        ListView.as_view(model=Person),
        name='person_list'
    ),
    url(
        r'^person_detail/(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=Person),
        name='person_detail'
    ),
    url(
        r'^person_autocomplete/$',
        login_required(Select2QuerySetView.as_view(model=Person, create_field='name')),
        name='person_autocomplete'
    ),
    url(
        r'^movie_list/$',
        ListView.as_view(
            model=Movie,
            queryset=Movie.objects.prefetch_related('attendees').select_related('picker')),
        name='movie_list'
    ),
    url(
        r'^movie_add/$',
        login_required(MovieCreateView.as_view()),
        name='movie_add'
    ),
    url(
        r'^movie_edit/(?P<pk>[0-9]+)/$',
        login_required(MovieUpdateView.as_view()),
        name='movie_edit'
    )
]
