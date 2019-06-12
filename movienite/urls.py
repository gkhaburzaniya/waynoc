from django.urls import path

from .views import (person_list, person_detail, person_edit, movie_list,
                    movie_add, movie_edit, movie_delete, person_delete)

app_name = 'movienite'
urlpatterns = [
    path('', person_list, name='person_list'),
    path('person_detail/<int:pk>/', person_detail, name='person_detail'),
    path('person_edit/<int:pk>/', person_edit, name='person_edit'),
    path('person_delete/<int:pk>', person_delete, name='person_delete'),
    path('movie_list/', movie_list, name='movie_list'),
    path('movie_add/', movie_add, name='movie_add'),
    path('movie_edit/<int:pk>/', movie_edit, name='movie_edit'),
    path('movie_delete/<int:pk>', movie_delete, name='movie_delete')
]
