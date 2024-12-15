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
            1: [

            ]
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


class Attribute:
    def __init__(self, short_name, value):
        self.short_name = short_name
        self._value = span(value)
        self.element = span(f"{self.short_name}:", self._value)

    @property
    def value(self):
        return self._value.textContent

    @value.setter
    def value(self, value):
        self._value.textContent = value


class Age(Attribute):
    @property
    def value(self):
        return float(self._value.textContent)

    @value.setter
    def value(self, value):
        self._value.textContent = value

    def __add__(self, other):
        return self.value + other


class Characteristic(Attribute):

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

    # TODO: add shouldn't be updating..., could at least change it to iadd
    def __add__(self, other):
        self.value += other
        self.effect_text = self._change_characteristic(other)
        return self


@dataclass(frozen=True)
class Virtue:
    name: str
    description: str
    type: str
    cost: int


hermetic_magus = Virtue(name="Hermetic_Magus",
                        description=page["#hermetic_magus_description"][0].textContent,
                        type="Social Status",
                        cost=0)


class Player:

    def __init__(self):
        self.intelligence = Characteristic("Int", -10)
        self.perception = Characteristic("Per", -10)
        self.strength = Characteristic("Str", -10)
        self.stamina = Characteristic("Sta", -10)
        self.presence = Characteristic("Prs", -10)
        self.communication = Characteristic("Com", -10)
        self.dexterity = Characteristic("Dex", -10)
        self.quickness = Characteristic("Qik", -10)

        self.name = Attribute("Name", "")
        self.age = Age("Age", 0)
        self.house = Attribute("House", "")
        self.virtues = ["Hermetic Magus"]
        self.flaws = []

        self.text = [EventText("You are born", "")]
        self.childhood = Childhood(self)

    # def __getattribute__(self, name):
    #     attribute = super().__getattribute__(name)
    #     if not issubclass(type(attribute), Attribute):
    #         return attribute
    #     elif name not in self.placed:
    #         self.placed.add(name)
    #         return attribute
    #     else:
    #         return attribute.value

    def change_name(self, new_name):
        self.name.value = new_name
        self.effect_text = f"Your name is {new_name}"
        return self


def start(_):
    global Events
    main.append(board)
    Events = events


def custom_character(_):
    start_button.remove()
    custom_character_button.remove()
    CharacterCreation().start()


def advance(_):
    player.age.value += .25
    player.text = [EventText(event.flavor, event.effect().effect_text)
                   for event in player.childhood[player.age.value]]
    update_state()


def restart(_):
    global player, board
    player = Player()
    board.remove()
    board = new_board()
    start(_)


class CharacterCreation:

    def __init__(self):
        self.house_selection = div(
            p("Which Hermetic House do you hail from?"),
            p(
                button("Bjornaer",
                       type="submit",
                       classes=["btn", "btn-secondary"],
                       on_click=self.house_choice),
                page["#bjornaer_description"][0].textContent
            ),
            p(
                button("Bonisagus",
                       type="submit",
                       classes=["btn", "btn-secondary"],
                       on_click=self.house_choice),
                page["#bonisagus_description"][0].textContent
            ),
            p(
                button("Criamon",
                       type="submit",
                       classes=["btn", "btn-secondary"],
                       on_click=self.house_choice),
                page["#criamon_description"][0].textContent
            ),
            classes=["col"])
        self.virtues_and_flaws_selection = div(
            "What are your virtues and flaws?",
            p(
                button(hermetic_magus,
                       type="submit",
                       classes=["btn", "btn-secondary"],
                       on_click=self.virtues_and_flaws_choice),
                hermetic_magus.description,
                hermetic_magus.type,
                hermetic_magus.cost
            ),
        )

    def start(self):
        main.append(self.house_selection)

    def house_choice(self, e):
        player.house.value = e.target.textContent
        self.house_selection.remove()
        main.append(self.virtues_and_flaws_selection)

    def virtues_and_flaws_choice(self, e):
        self.virtues_and_flaws_selection.remove()
        start(e)


page["#loading"][0].remove()
main = page["main"][0]
start_button = button("Start",
                      type="submit",
                      classes=["btn", "btn-secondary"],
                      on_click=start)
custom_character_button = button("Custom Character",
                                 type="submit",
                                 classes=["btn", "btn-secondary"],
                                 on_click=custom_character)

# TODO: get events to display right
events = div()

player = Player()


def new_board():
    return div(
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
                        td(h5(player.name.element)),
                        td(h5(player.age.element)),
                        td(h5(player.house.element)),
                    )
                ),
                classes=["table", "table-borderless", "table-sm"]
            ),
            classes=["col"]
        ),
        events,
        classes=["row", "col-md-8", "offset-md-2"]
    )


board = new_board()

main.append(start_button, custom_character_button)


def update_state():
    events.innerHTML = ""
    for event in player.text:
        events.innerHTML += event.flavor_text + "<br>"
        events.innerHTML += "<b>" + event.effect_text + "</b><br>"
