""" Game logic goes here """
import random

from dataclasses import dataclass


@dataclass(eq=False)
class Player:

    age: int = 0
    alive: bool = True

    @property
    def text(self):
        if not player.alive:
            return "You are dead"
        return flavor_text.get(self.age)


player = Player()


def advance_year():
    if not player.alive:
        player.age = -1
        player.alive = True
    player.age += 1
    if random.randint(0, 10) == 0:
        player.alive = False


flavor_text = {0: "You are born",
               1:
"""This year you learned to smile.
To bring your hands to your mouth and suck on your hand.
To look around.
To coo.
To move your head
To recognize faces"""}
