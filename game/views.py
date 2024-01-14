from django.shortcuts import render
from django.views import View


class Game(View):
    template_name = 'game/game.html'

    @classmethod
    def get(cls, request):
        return render(request, cls.template_name)
