from django.urls import path

from .views import (PersonList, PersonDetail, PersonEdit, MovieList, MovieAdd,
                    MovieEdit, MovieDelete)

app_name = 'movienite'
urlpatterns = [
    path('', PersonList, name='person_list'),
    path('person_detail/<int:pk>/', PersonDetail, name='person_detail'),
    path('person_edit/<int:pk>/', PersonEdit, name='person_edit'),
    path('movie_list/', MovieList, name='movie_list'),
    path('movie_add/', MovieAdd, name='movie_add'),
    path('movie_edit/<int:pk>/', MovieEdit, name='movie_edit'),
    path('movie_delete/<int:pk>', MovieDelete, name='movie_delete')
]
