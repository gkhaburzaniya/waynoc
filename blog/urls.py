from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .models import Post

app_name = 'blog'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Post, ordering='-published_date'),
        name='post_list'),
    url(r'^add/$', CreateView.as_view(model=Post, fields=['title', 'text'],
                                      success_url=reverse_lazy('blog:post_list')),
        name='post_add'),
]
