from dataclasses import dataclass
from functools import partial

from pyscript.web import (
    page,
    input_,
    div,
    button,
    p,
    span,
    table,
    tbody,
    tr,
    td,
    h5,
    label,
    strong,
    form,
    em,
)


class Childhood:

    def __init__(self, player):
        self.events = {
            0.25: [
                Event(
                    "You learned to recognize faces.",
                    partial(player.intelligence.__iadd__, 1),
                ),
                Event("To look around.", partial(player.perception.__iadd__, 1)),
                Event("To lift your head.", partial(player.strength.__iadd__, 1)),
                Event("To hold your head steady.", partial(player.stamina.__iadd__, 1)),
                Event("To smile at people.", partial(player.presence.__iadd__, 1)),
                Event("To coo and babble.", partial(player.communication.__iadd__, 1)),
                Event("To suck on your hand.", partial(player.dexterity.__iadd__, 1)),
                Event(
                    "To swing at dangling toys.", partial(player.quickness.__iadd__, 1)
                ),
            ],
            0.5: [
                Event("You learned your name.", partial(player.change_name, "George")),
                Event(
                    "You learned to put things in your mouth.",
                    partial(player.perception.__iadd__, 1),
                ),
                Event("To sit and roll over.", partial(player.strength.__iadd__, 1)),
                Event(
                    "To cry in different ways.",
                    partial(player.communication.__iadd__, 1),
                ),
                Event("To reach for things.", partial(player.dexterity.__iadd__, 1)),
                Event("To crawl.", partial(player.quickness.__iadd__, 1)),
            ],
            0.75: [
                Event(
                    "You learned to fear strangers.",
                    partial(player.intelligence.__iadd__, 1),
                ),
                Event(
                    "To look for hidden things", partial(player.perception.__iadd__, 1)
                ),
                Event(
                    "To stand while holding on to something",
                    partial(player.strength.__iadd__, 1),
                ),
                Event(
                    "To understand simple sentences, make many sounds and "
                    "simple gestures",
                    partial(player.communication.__iadd__, 1),
                ),
                Event(
                    "To pick things up and move them between your hands",
                    partial(player.dexterity.__iadd__, 1),
                ),
            ],
            1: [Event("You turn 1! Not that you can count")],
        }

    def __getitem__(self, item):
        return self.events[item]


@dataclass(frozen=True)
class Event:
    flavor: str
    effect: partial = lambda: EventText("", "")


@dataclass(frozen=True)
class EventText:
    flavor_text: str
    effect_text: str


class OnScreenValue:
    def __init__(self, short_name, value):
        self.short_name = short_name
        self._value = span(value)
        self.element = span(f"{self.short_name}: ", self._value)

    @property
    def value(self):
        return self._value.textContent

    @value.setter
    def value(self, value):
        self._value.textContent = value


class Age(OnScreenValue):
    @property
    def value(self):
        return float(self._value.textContent)

    @value.setter
    def value(self, value):
        self._value.textContent = value

    def __add__(self, other):
        return self.value + other


class Characteristic(OnScreenValue):

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

    def __iadd__(self, other):
        self.value += other
        self.effect_text = self._change_characteristic(other)
        return self


@dataclass
class Virtue:
    name: str
    description: str
    type: str
    cost: int
    checked: bool = False
    disabled: bool = False
    hidden: bool = False

    def __post_init__(self):
        self.label = div(
            input_(
                type="radio",
                classes=["form-check-input"],
                checked=self.checked,
                disabled=self.disabled,
            ),
            label(
                f"{self.name}:",
                self.description,
                em(f"{self.type}. "),
                strong(f"Cost: {self.cost}"),
                classes=["form-check-radio"],
            ),
            hidden=self.hidden,
            classes=["form-check"])


hermetic_magus = Virtue(
    name="Hermetic Magus",
    description=page["#hermetic_magus_description"][0].textContent,
    type="Social Status",
    cost=0,
    checked=True,
    disabled=True,
)
the_gift = Virtue(
    name="The Gift",
    description=page["#the_gift_description"][0].textContent,
    type="Special",
    cost=0,
    checked=True,
    disabled=True,
)
heartbeast = Virtue(
    name="Heartbeast",
    description=page["#heartbeast_description"][0].textContent,
    type="Hermetic",
    cost=1,
    checked=True,
    disabled=True,
    hidden=True
)
puissant_magic_theory = Virtue(
    name="Puissant Magic Theory",
    description=page["#puissant_magic_theory_description"][0].textContent,
    type="General",
    cost=1,
)


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

        self.name = OnScreenValue("Name", "")
        self.age = Age("Age", 0)
        self.house = OnScreenValue("House", "")
        self.virtues = [hermetic_magus, the_gift]
        self.flaws = []

        self.text = [EventText("You are born", "")]
        self.childhood = Childhood(self)

    def change_name(self, new_name):
        self.name.value = new_name
        self.effect_text = f"Your name is {new_name}"
        return self


def start(_):
    start_button.remove()
    custom_character_button.remove()
    main.append(board)


def custom_character(_):
    start_button.remove()
    custom_character_button.remove()
    CharacterCreation().start()


def advance(_):
    player.age.value += 0.25
    player.text = [
        EventText(event.flavor, event.effect().effect_text)
        for event in player.childhood[player.age.value]
    ]
    update_state()


def restart(_):
    global player, board
    player = Player()
    board.remove()
    board = new_board()
    start(_)


class CharacterCreation:
    virtue_points_available = OnScreenValue("Virtue Points Available", 0)
    virtue_points_from_flaws = OnScreenValue("Points From Flaws (Max 10)", 0)

    def __init__(self):
        self.house_selection = div(
            p("Which Hermetic House do you hail from?"),
            p(
                button(
                    "Bjornaer",
                    type="submit",
                    classes=["btn", "btn-secondary"],
                    on_click=self.house_choice,
                ),
                page["#bjornaer_description"][0].textContent,
            ),
            p(
                button(
                    "Bonisagus",
                    type="submit",
                    classes=["btn", "btn-secondary"],
                    on_click=self.house_choice,
                ),
                page["#bonisagus_description"][0].textContent,
            ),
            p(
                button(
                    "Criamon",
                    type="submit",
                    classes=["btn", "btn-secondary"],
                    on_click=self.house_choice,
                ),
                page["#criamon_description"][0].textContent,
            ),
            classes=["col"],
        )
        self.virtues_and_flaws_selection = div(
            "What are your virtues and flaws?",
            table(
                tbody(
                    tr(
                        td(h5(CharacterCreation.virtue_points_available.element)),
                        td(h5(CharacterCreation.virtue_points_from_flaws.element)),
                    )
                ),
                classes=["table", "table-borderless", "table-sm"],
            ),
            form(
                hermetic_magus.label,
                the_gift.label,
                heartbeast.label,
                puissant_magic_theory.label,
            ),
        )

    def start(self):
        main.append(self.house_selection)

    def house_choice(self, e):
        player.house.value = e.target.textContent
        self.house_selection.remove()
        if player.house.value == "Bjornaer":
            heartbeast.label.hidden = False
        elif player.house.value == "Bonisagus":
            puissant_magic_theory.label["input"].checked = True
            puissant_magic_theory.label["input"].disabled = True
        main.append(self.virtues_and_flaws_selection)

    def virtues_and_flaws_choice(self, e):
        self.virtues_and_flaws_selection.remove()
        start(e)


page["#loading"][0].remove()
main = page["main"][0]
start_button = button(
    "Start", type="submit", classes=["btn", "btn-secondary"], on_click=start
)
custom_character_button = button(
    "Custom Character",
    type="submit",
    classes=["btn", "btn-secondary"],
    on_click=custom_character,
)

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
                classes=[
                    "table",
                    "table-striped",
                    "table-borderless",
                    "table-hover",
                    "table-sm",
                ],
            ),
            classes=["col-4", "col-md-2"],
        ),
        div(
            button(
                "Next Season",
                type="submit",
                classes=["btn", "btn-secondary"],
                on_click=advance,
            ),
            button(
                "Restart",
                type="submit",
                classes=["btn", "btn-secondary"],
                on_click=restart,
            ),
            table(
                tbody(
                    tr(
                        td(h5(player.name.element)),
                        td(h5(player.age.element)),
                        td(h5(player.house.element)),
                    )
                ),
                classes=["table", "table-borderless", "table-sm"],
            ),
            events,
            classes=["col"],
        ),
        classes=["row", "col-md-8", "offset-md-2"],
    )


board = new_board()

main.append(start_button, custom_character_button)


def update_state():
    events.innerHTML = ""
    for event in player.text:
        events.innerHTML += event.flavor_text + "<br>"
        events.innerHTML += "<b>" + event.effect_text + "</b><br>"
