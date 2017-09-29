from django.conf.urls import url
from django.views.generic import ListView, DetailView

from .models import Person, Event

app_name = 'movienite'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Person), name='person_list'),
    url(r'^person_detail/(?P<pk>[0-9]+)/$', ListView.as_view(model=Person), name='person_detail'),
    url(r'^event_list/$', DetailView.as_view(model=Event), name='event_list'),
]
