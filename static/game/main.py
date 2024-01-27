from dataclasses import dataclass
from functools import partial

from pyweb import pydom


class Childhood:

    def __init__(self, player):
        self.events = {
            1/4: [
                Event("You learned to recognize faces.",
                      partial(player.intelligence.__add__, 1)),
                Event("To look around.",
                      partial(player.perception.__add__, 1)),
                Event("To lift your head.",
                      partial(player.strength.__add__, 1)),
                Event("To hold your head steady.",
                      partial(player.stamina.__add__, 1)),
                Event("To smile at people.",
                      partial(player.presence.__add__, 1)),
                Event("To coo and babble.",
                      partial(player.communication.__add__, 1)),
                Event("To suck on your hand.",
                      partial(player.dexterity.__add__, 1)),
                Event("To swing at dangling toys.",
                      partial(player.quickness.__add__, 1)),
            ],
            2/4: [
                Event("You learned your name.",
                      partial(player.change_name, "George")),
                Event("You learned to put things in your mouth.",
                      partial(player.perception.__add__, 1)),
                Event("To sit and roll over.",
                      partial(player.strength.__add__, 1)),
                Event("To cry in different ways.",
                      partial(player.communication.__add__, 1)),
                Event("To reach for things.",
                      partial(player.dexterity.__add__, 1)),
                Event("To crawl.",
                      partial(player.quickness.__add__, 1)),
            ],
            3/4: [
                Event("You learned to fear strangers.",
                      partial(player.intelligence.__add__, 1)),
                Event("To look for hidden things",
                      partial(player.perception.__add__, 1)),
                Event("To stand while holding on to something",
                      partial(player.strength.__add__, 1)),
                Event("To understand simple sentences, make many sounds and "
                      "simple gestures",
                      partial(player.communication.__add__, 1)),
                Event("To pick things up and move them between your hands",
                      partial(player.dexterity.__add__, 1)),
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


class Characteristic:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        pydom[f'#{self.name}'][0].text = f'{self.name}: {value}'

    def _change_characteristic(self, change):
        if change > 0:
            return f"+{change} {self.name}"
        elif change < 0:
            return f"{change} {self.name}"
        else:
            raise ValueError

    def __add__(self, other):
        self.value += other
        self.effect_text = self._change_characteristic(other)
        return self


@dataclass(eq=False)
class Player:

    name: str = ""
    age: float = 0
    text: list = (EventText("You are born", ""),)

    def __init__(self):
        self.intelligence = Characteristic("Int", -10)
        self.perception = Characteristic("Per", -10)
        self.strength = Characteristic("Str", -10)
        self.stamina = Characteristic("Sta", -10)
        self.presence = Characteristic("Prs", -10)
        self.communication = Characteristic("Com", -10)
        self.dexterity = Characteristic("Dex", -10)
        self.quickness = Characteristic("Qik", -10)
        self.childhood = Childhood(self)

    def change_name(self, new_name):
        self.name = new_name
        self.effect_text = f"Your name is {new_name}"
        return self


Events = pydom["#Events"][0]
player = Player()


def update_state():
    pydom["#Name"][0].text = player.name
    pydom["#Age"][0].text = player.age
    Events.html = ""
    for event in player.text:
        Events.html += event.flavor_text + "<br>"
        Events.html += "<b>" + event.effect_text + "</b><br>"


def advance(e):
    player.age += 0.25
    player.text = [EventText(event.flavor, event.effect().effect_text)
                   for event in player.childhood[player.age]]
    update_state()


def restart(e):
    global player
    player = Player()
    update_state()

