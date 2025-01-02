from django.urls import path
from .views import Ars

app_name = "ars"
urlpatterns = [path("", Ars.as_view(), name="ars")]
