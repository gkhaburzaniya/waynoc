from django.conf.urls import url
from django.views.generic import ListView, DetailView

from .models import Post

urlpatterns = [
    url(r'^$', ListView.as_view(model=Post), name='post_list'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Post), name='post_detail')
]
