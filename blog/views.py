from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Post

post_list = ListView.as_view(model=Post, ordering="-date")

post_add = permission_required("blog.add_post")(
    CreateView.as_view(
        model=Post,
        fields=["title", "date", "text"],
        success_url=reverse_lazy("blog:post_list"),
    )
)

post_edit = permission_required("blog.change_post")(
    UpdateView.as_view(
        model=Post,
        fields=["title", "date", "text"],
        success_url=reverse_lazy("blog:post_list"),
    )
)

post_delete = permission_required("blog.delete_post")(
    DeleteView.as_view(model=Post, success_url=reverse_lazy("blog:post_list"))
)
