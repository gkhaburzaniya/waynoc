from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("blog/", include("blog.urls")),
    path("ars/", include("ars.urls")),
    path("prototype", include("prototype.urls")),
    path("", include("movienite.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
