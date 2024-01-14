from dataclasses import dataclass
from functools import partial

from pyweb import pydom


class Childhood:

    def __init__(self, player):
        self.events = {
            1/4: [
                Event("You learned to recognize faces.",
                      partial(player.change_intelligence, 1)),
                Event("To look around.",
                      partial(player.change_perception, 1)),
                Event("To lift your head.",
                      partial(player.change_strength, 1)),
                Event("To hold your head steady.",
                      partial(player.change_stamina, 1)),
                Event("To smile at people.",
                      partial(player.change_presence, 1)),
                Event("To coo and babble.",
                      partial(player.change_communication, 1)),
                Event("To suck on your hand.",
                      partial(player.change_dexterity, 1)),
                Event("To swing at dangling toys.",
                      partial(player.change_quickness, 1)),
            ],
            1/2: [
                Event("You learned your name.",
                      partial(player.change_name, "George")),
                Event("You learned to put things in your mouth.",
                      partial(player.change_perception, 1)),
                Event("To sit and roll over.",
                      partial(player.change_strength, 1)),
                Event("To cry in different ways.",
                      partial(player.change_communication, 1)),
                Event("To reach for things.",
                      partial(player.change_dexterity, 1)),
                Event("To crawl.",
                      partial(player.change_quickness, 1)),
            ],
            3/4: [
                Event("You learned to fear strangers.",
                      partial(player.change_intelligence, 1)),
                Event("To look for hidden things",
                      partial(player.change_perception, 1)),
                Event("To stand while holding on to something",
                      partial(player.change_strength, 1)),
                Event("To understand simple sentences, make many sounds and "
                      "simple gestures",
                      partial(player.change_communication, 1)),
                Event("To pick things up and move them between your hands",
                      partial(player.change_dexterity, 1)),
            ],
        }

    def __getitem__(self, item):
        return self.events[item]


@dataclass(frozen=True)
class Event:
    flavor: str
    effect: partial


@dataclass(frozen=True)
class EventText:
    flavor_text: str
    effect_text: str


@dataclass(eq=False)
class Player:

    name: str = ""
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

    def __post_init__(self):
        self.childhood = Childhood(self)

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

    def change_name(self, new_name):
        self.name = new_name
        return f"Your name is {new_name}"

    @staticmethod
    def _change_characteristic(characteristic, change):
        if change > 0:
            return f"+{change} {characteristic}"
        elif change < 0:
            return f"{change} {characteristic}"
        else:
            raise ValueError


Int = pydom["#Int"][0]._js

player = Player()


# def advance():
#     player.age += 0.25
#     player.text = [EventText(event.flavor, event.effect())
#                    for event in player.childhood[player.age]]
#

def restart():
    global player
    player = Player()


def advance(e):
    # create task
    Int.textContent = "Test5"
