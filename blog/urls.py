from django.urls import path

from .views import PostList, PostAdd, PostEdit, PostDelete

app_name = 'blog'
urlpatterns = [
    path('', PostList, name='post_list'),
    path('add/', PostAdd, name='post_add'),
    path('post_edit/<int:pk>/', PostEdit, name='post_edit'),
    path('movie_delete/<int:pk>/', PostDelete, name='post_delete')
]
