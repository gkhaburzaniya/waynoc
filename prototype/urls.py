from django.urls import path
from .views import Prototype

app_name = "prototype"
urlpatterns = [path("", Prototype.as_view(), name="prototype")]
