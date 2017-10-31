from django.urls import reverse_lazy
from django.conf.urls import url
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from .forms import MovieForm
from .models import Person, Movie

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
        r'^movie_list/$',
        ListView.as_view(
            model=Movie,
            queryset=Movie.objects.prefetch_related('attendees').select_related('picker')),
        name='movie_list'
    ),
    url(
        r'^movie_add/$',
        login_required(CreateView.as_view(model=Movie, form_class=MovieForm)),
        name='movie_add'
    ),
    url(
        r'^movie_edit/(?P<pk>[0-9]+)/$',
        login_required(UpdateView.as_view(model=Movie, form_class=MovieForm)),
        name='movie_edit'
    ),
    url(
        r'^movie_delete/(?P<pk>[0-9]+)/$',
        login_required(DeleteView.as_view(model=Movie,
                                          success_url=reverse_lazy('movienite:movie_list'))),
        name='movie_delete'
    )
]
