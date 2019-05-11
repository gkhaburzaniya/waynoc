from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.decorators import permission_required


PostList = ListView.as_view(model=Post, ordering='-date')

PostAdd = permission_required('blog.add_post')(
    CreateView.as_view(model=Post, fields=['title', 'date', 'text'],
                       success_url=reverse_lazy('blog:post_list')))

PostEdit = permission_required('blog.change_post')(
    UpdateView.as_view(model=Post, fields=['title', 'date', 'text'],
                       success_url=reverse_lazy('blog:post_list')))

PostDelete = permission_required('blog.delete_post')(
    DeleteView.as_view(model=Post, success_url=reverse_lazy('blog:post_list')))
