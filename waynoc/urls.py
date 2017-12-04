from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('', include('movienite.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
