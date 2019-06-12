from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, ListView, UpdateView,
                                  DeleteView)

from .forms import MovieForm
from .models import Person, Movie

person_list = ListView.as_view(model=Person)
person_detail = DetailView.as_view(model=Person)
person_edit = permission_required('movienite.change_person')(
    UpdateView.as_view(model=Person, fields=['name']))
person_delete = permission_required('movienite.delete_person')(
    DeleteView.as_view(model=Person,
                       success_url=reverse_lazy('movienite:person_list'),
                       template_name='movienite/confirm_delete.html'))

movie_list = ListView.as_view(
    model=Movie,
    queryset=Movie.objects.prefetch_related(
        'attendees').select_related('picker'))
movie_add = permission_required('movienite.add_movie')(
    CreateView.as_view(model=Movie, form_class=MovieForm,
                       success_url=reverse_lazy('movienite:movie_list')))
movie_edit = permission_required('movienite.change_movie')(
    UpdateView.as_view(model=Movie, form_class=MovieForm,
                       success_url=reverse_lazy('movienite:movie_list')))
movie_delete = permission_required('movienite.delete_movie')(
    DeleteView.as_view(model=Movie,
                       success_url=reverse_lazy('movienite:movie_list'),
                       template_name='movienite/confirm_delete.html'))
