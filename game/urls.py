from django.urls import path
from .views import Game

app_name = "game"
urlpatterns = [path("", Game.as_view(), name="game")]
