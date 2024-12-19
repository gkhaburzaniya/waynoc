from django.urls import path

from .views import post_list, post_add, post_edit, post_delete

app_name = "blog"
urlpatterns = [
    path("", post_list, name="post_list"),
    path("add/", post_add, name="post_add"),
    path("post_edit/<int:pk>/", post_edit, name="post_edit"),
    path("post_delete/<int:pk>/", post_delete, name="post_delete"),
]
