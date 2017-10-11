from django.urls import reverse_lazy
from django.conf.urls import url
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required

from .models import Post

app_name = 'blog'
urlpatterns = [
    url(r'^$', ListView.as_view(model=Post, ordering='-date'),
        name='post_list'),
    url(r'^add/$', login_required(CreateView.as_view(model=Post, fields=['title', 'text'],
                                                     success_url=reverse_lazy('blog:post_list'))),
        name='post_add'),
]
