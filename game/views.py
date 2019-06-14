from django.shortcuts import render
from django.views import View

import game


class Game(View):
    template_name = 'game/game.html'

    @classmethod
    def get(cls, request):
        context = {'age': game.player.age,
                   'text': game.player.text}
        return render(request, cls.template_name, context=context)

    @classmethod
    def post(cls, request):
        action = request.POST['action']
        actions[action]()
        return cls.get(request)


actions = {'advance': game.advance,
           'restart': game.restart}
