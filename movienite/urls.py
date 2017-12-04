from django.urls import reverse_lazy, path
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from .forms import MovieForm
from .models import Person, Movie

app_name = 'movienite'
urlpatterns = [
    path(
        '',
        ListView.as_view(model=Person),
        name='person_list'
    ),
    path(
        'person_detail/<int:pk>/',
        DetailView.as_view(model=Person),
        name='person_detail'
    ),
    path(
        'person_edit/<int:pk>/',
        login_required(UpdateView.as_view(model=Person, fields=['name'])),
        name='person_edit'
    ),
    path(
        'movie_list/',
        ListView.as_view(
            model=Movie,
            queryset=Movie.objects.prefetch_related('attendees').select_related('picker')),
        name='movie_list'
    ),
    path(
        'movie_add/',
        login_required(CreateView.as_view(model=Movie,
                                          form_class=MovieForm,
                                          success_url=reverse_lazy('movienite:movie_list'))),
        name='movie_add'
    ),
    path(
        'movie_edit/<int:pk>/',
        login_required(UpdateView.as_view(model=Movie,
                                          form_class=MovieForm,
                                          success_url=reverse_lazy('movienite:movie_list'))),
        name='movie_edit'
    ),
    path(
        'movie_delete/<int:pk>',
        login_required(DeleteView.as_view(model=Movie,
                                          success_url=reverse_lazy('movienite:movie_list'))),
        name='movie_delete'
    )
]
