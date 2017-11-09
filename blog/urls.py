from django.urls import reverse_lazy
from django.conf.urls import url
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import permission_required

from .models import Post

app_name = 'blog'
urlpatterns = [
    url(
        r'^$',
        ListView.as_view(model=Post, ordering='-date'),
        name='post_list'
    ),
    url(
        r'^add/$',
        permission_required('blog.add_post')(CreateView.as_view(
            model=Post,
            fields=['title', 'date', 'text'],
            success_url=reverse_lazy('blog:post_list')
        )),
        name='post_add'
    ),
    url(
        r'^post_edit/(?P<pk>[0-9]+)/$',
        permission_required('blog.change_post')(UpdateView.as_view(
            model=Post,
            fields=['title', 'date', 'text'])
        ),
        name='post_edit'
    ),
    url(
        r'^movie_delete/(?P<pk>[0-9]+)/$',
        permission_required('blog.delete_post')(DeleteView.as_view(
            model=Post,
            success_url=reverse_lazy('blog:post_list')
        )),
        name='post_delete'
    )
]
