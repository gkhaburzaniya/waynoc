from django.urls import reverse_lazy
from django.conf.urls import url
from django.views.generic import ListView, DetailView, CreateView

from .models import Person, Movie

app_name = 'movienite'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Person, ordering='-score'),
        name='person_list'),
    url(r'^person_detail/(?P<pk>[0-9]+)/$', DetailView.as_view(model=Person),
        name='person_detail'),
    url(r'^movie_list/$', ListView.as_view(model=Movie, ordering='-date'),
        name='movie_list'),
    url(r'^movie_add/$', CreateView.as_view(model=Movie, fields=['title', 'picker', 'attendees'],
                                            success_url=reverse_lazy('movienite:movie_list')),
        name='movie_add'),
    url(r'^person_add/$', CreateView.as_view(model=Person, fields=['name'],
                                             success_url=reverse_lazy('movienite:person_list')),
        name='movie_add'),
]
