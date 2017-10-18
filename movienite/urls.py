from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from .models import Person, Movie
from .views import MovieCreateView

app_name = 'movienite'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Person),
        name='person_list'),
    url(r'^person_detail/(?P<pk>[0-9]+)/$', DetailView.as_view(model=Person),
        name='person_detail'),
    url(r'^movie_list/$', ListView.as_view(
            model=Movie,
            queryset=Movie.objects.prefetch_related('attendees')
                                  .select_related('picker')),
        name='movie_list'),
    url(r'^movie_add/$', login_required(MovieCreateView.as_view()),
        name='movie_add'),
]
