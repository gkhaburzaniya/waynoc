from django.shortcuts import render
from django.views import View

import game


class Game(View):
    template_name = 'game/game.html'

    @classmethod
    def get(cls, request):
        context = {'player': game.player}
        return render(request, cls.template_name, context=context)


actions = {'advance': game.advance,
           'restart': game.restart}
