from django.urls import reverse_lazy, path
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required

from .models import Post

app_name = 'blog'
urlpatterns = [
    path(
        '',
        ListView.as_view(model=Post, ordering='-date'),
        name='post_list'
    ),
    path(
        'add/',
        permission_required('blog.add_post')(CreateView.as_view(
            model=Post,
            fields=['title', 'date', 'text'],
            success_url=reverse_lazy('blog:post_list')
        )),
        name='post_add'
    ),
    path(
        'post_edit/<int:pk>/',
        permission_required('blog.change_post')(UpdateView.as_view(
            model=Post,
            fields=['title', 'date', 'text'],
            success_url=reverse_lazy('blog:post_list'))
        ),
        name='post_edit'
    ),
    path(
        'movie_delete/<int:pk>/',
        permission_required('blog.delete_post')(DeleteView.as_view(
            model=Post,
            success_url=reverse_lazy('blog:post_list')
        )),
        name='post_delete'
    )
]
