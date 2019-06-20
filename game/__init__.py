""" Game logic goes here """

from dataclasses import dataclass
from collections import namedtuple
from functools import partial

EventText = namedtuple('EventText', ['flavor_text', 'effect_text'])
Event = namedtuple('Event', ['flavor', 'effect'])


@dataclass(eq=False)
class Player:

    age: float = 0
    text: list = (EventText("You are born", ""),)

    # characteristics
    intelligence: int = -10
    perception: int = -10
    strength: int = -10
    stamina: int = -10
    presence: int = -10
    communication: int = -10
    dexterity: int = -10
    quickness: int = -10

    @property
    def childhood(self):
        return {
            1/4: [
                Event("You learned to recognize faces.",
                      partial(self.change_intelligence, 1)),
                Event("To look around.",
                      partial(self.change_perception, 1)),
                Event("To lift your head.",
                      partial(self.change_strength, 1)),
                Event("To hold your head steady.",
                      partial(self.change_stamina, 1)),
                Event("To smile at people.",
                      partial(self.change_presence, 1)),
                Event("To coo and babble.",
                      partial(self.change_communication, 1)),
                Event("To suck on your hand.",
                      partial(self.change_dexterity, 1)),
                Event("To swing at dangling toys.",
                      partial(self.change_quickness, 1))
            ],
            1/2: [
                Event("You learned your name.",
                      partial(self.change_intelligence, 1)),
                Event("You learned to put things in your mouth.",
                      partial(self.change_perception, 1)),
                Event("To sit and roll over.",
                      partial(self.change_strength, 1)),
                Event("To cry in different ways.",
                      partial(self.change_communication, 1)),
                Event("To reach for things.",
                      partial(self.change_dexterity, 1)),
                Event("To crawl.",
                      partial(self.change_quickness, 1))
            ]
}

    def change_intelligence(self, change):
        self.intelligence += change
        return self._change_characteristic("Intelligence", change)

    def change_perception(self, change):
        self.perception += change
        return self._change_characteristic("Perception", change)

    def change_strength(self, change):
        self.strength += change
        return self._change_characteristic("Strength", change)

    def change_stamina(self, change):
        self.stamina += change
        return self._change_characteristic("Stamina", change)

    def change_presence(self, change):
        self.presence += change
        return self._change_characteristic("Presence", change)

    def change_communication(self, change):
        self.communication += change
        return self._change_characteristic("Communication", change)

    def change_dexterity(self, change):
        self.dexterity += change
        return self._change_characteristic("Dexterity", change)

    def change_quickness(self, change):
        self.quickness += change
        return self._change_characteristic("Quickness", change)

    @staticmethod
    def _change_characteristic(characteristic, change):
        if change > 0:
            return f"+{change} {characteristic}"
        elif change < 0:
            return f"{change} {characteristic}"
        else:
            raise ValueError


player = Player()


def advance():
    player.age += 0.25
    player.text = [EventText(event.flavor, event.effect())
                   for event in player.childhood[player.age]]


def restart():
    global player
    player = Player()
