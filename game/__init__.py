""" Game logic goes here """

from .player import Player
from .events import EventText

player = Player()


def advance():
    player.age += 0.25
    player.text = [EventText(event.flavor, event.effect())
                   for event in player.childhood[player.age]]


def restart():
    global player
    player = Player()
