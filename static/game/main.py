from dataclasses import dataclass
from functools import partial

from pyscript.web import page, div, button, p, span, table, tbody, tr, td, h5


class Childhood:

    def __init__(self, player):
        self.events = {
            1 / 4: [
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
            2 / 4: [
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
            3 / 4: [
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
    def __init__(self, short_name, value):
        self.short_name = short_name
        self._value = span(value)
        self.element = span(self.short_name, self._value)

    @property
    def value(self):
        return int(self._value.textContent)

    @value.setter
    def value(self, value):
        self._value.textContent = value

    def _change_characteristic(self, change):
        if change > 0:
            return f"+{change} {self.short_name}"
        elif change < 0:
            return f"{change} {self.short_name}"
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
    house: str = ""
    text: list = (EventText("You are born", ""),)

    def __init__(self):
        self.intelligence = Characteristic("Int", -10)
        self.perception = Characteristic("Per ", -10)
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


def start(_):
    global Events
    main.append(board)
    Events = events


def custom_character(_):
    main.append(house_selection)
    start_button.remove()
    custom_character_button.remove()


def advance(_):
    player.age += 0.25
    player.text = [EventText(event.flavor, event.effect().effect_text)
                   for event in player.childhood[player.age]]
    update_state()


# TODO: fix restart
def restart(_):
    global player
    player = Player()
    update_state()


def bjornaer_house_choice(e):
    player.house = house.textContent = e.target.textContent
    house_selection.remove()
    start(e)


main = page["main"][0]
start_button = button("Start",
                      type="submit",
                      classes=["btn", "btn-secondary"],
                      on_click=start)
custom_character_button = button("Custom Character",
                                 type="submit",
                                 classes=["btn", "btn-secondary"],
                                 on_click=custom_character)

name = span()
age = span()
house = span()

# TODO: get events to display right
events = div()

player = Player()

board = div(
    div(
        table(
            tbody(
                tr(td(player.intelligence.element)),
                tr(td(player.perception.element)),
                tr(td(player.strength.element)),
                tr(td(player.stamina.element)),
                tr(td(player.presence.element)),
                tr(td(player.communication.element)),
                tr(td(player.dexterity.element)),
                tr(td(player.quickness.element)),
            ),
            classes=["table", "table-striped", "table-borderless",
                     "table-hover", "table-sm"]
        ),
        classes=["col-4", "col-md-2"]
    ),
    div(
        button("Next Season",
               type="submit",
               classes=["btn", "btn-secondary"],
               on_click=advance),
        button("Restart",
               type="submit",
               classes=["btn", "btn-secondary"],
               on_click=restart),
        table(
            tbody(
                tr(
                    td(h5("Name: ", name)),
                    td(h5("Age: ", age)),
                    td(h5("House: ", house)),
                )
            ),
            classes=["table", "table-borderless", "table-sm"]
        ),
        classes=["col"]
    ),
    events,
    classes=["row", "col-md-8", "offset-md-2"]
)

house_selection = div(
    p("Which Hermetic House do you hail from?"),
    p(
        button("Bjornaer",
               type="submit",
               classes=["btn", "btn-secondary"],
               on_click=bjornaer_house_choice),
        page["#bjornaer_description"][0].textContent
    ),
    classes=["col"])

main.append(start_button, custom_character_button)


def update_state():
    name.textContent = player.name
    age.textContent = player.age
    events.innerHTML = ""
    for event in player.text:
        events.innerHTML += event.flavor_text + "<br>"
        events.innerHTML += "<b>" + event.effect_text + "</b><br>"

