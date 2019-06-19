""" Game logic goes here """

from dataclasses import dataclass
from collections import namedtuple
from functools import partial


@dataclass(eq=False)
class Player:

    age: float = 0

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
    def text(self):
        return childhood.get(self.age, [])

    def change_intelligence(self, change):
        self.intelligence += change
        self._change_characteristic("Intelligence", change)

    def change_perception(self, change):
        self.perception += change
        self._change_characteristic("Perception", change)

    def change_strength(self, change):
        self.strength += change
        self._change_characteristic("Strength", change)

    def change_stamina(self, change):
        self.stamina += change
        self._change_characteristic("Stamina", change)

    def change_presence(self, change):
        self.presence += change
        self._change_characteristic("Presence", change)

    def change_communication(self, change):
        self.communication += change
        self._change_characteristic("Communication", change)

    def change_dexterity(self, change):
        self.dexterity += change
        self._change_characteristic("Dexterity", change)

    def change_quickness(self, change):
        self.quickness += change
        self._change_characteristic("Quickness", change)

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
    for event in childhood[player.age]:
        event.effect()


def restart():
    global player
    player = Player()


Event = namedtuple('Event', ['flavor', 'effect'])
childhood = {
    0: [Event("You are born", str)],
    1/4: [
        Event("You learned to recognize faces.",
              partial(player.change_intelligence, 1)),
        Event("To look around.", partial(player.change_perception, 1)),
        Event("To move your head.", partial(player.change_strength, 1)),
        Event("To smile.", partial(player.change_presence, 1)),
        Event("To coo.", partial(player.change_communication, 1)),
        Event("To suck on your hand.", partial(player.change_dexterity, 1)),
    ]}
