from django.shortcuts import render
from django.views import View

from .game import player, advance_year


class Game(View):
    template_name = 'game/game.html'

    @classmethod
    def get(cls, request):
        context = {'age': player.age,
                   'text': player.text}
        return render(request, cls.template_name, context=context)

    @classmethod
    def post(cls, request):
        advance_year()
        return cls.get(request)
