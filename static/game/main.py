from dataclasses import dataclass, field
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
    select,
    option,
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


class OnScreenInt(OnScreenValue):
    @property
    def value(self):
        return int(self._value.textContent)

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


class Characteristic(OnScreenInt):

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
class House:
    name: str
    description: str

    def __post_init__(self):
        self.selection = select(hidden=True)


@dataclass
class Virtue:
    name: str
    type: str
    cost: int
    checked: bool = False
    disabled: bool = False
    hidden: bool = False
    options: list = field(default_factory=list)

    def __post_init__(self):
        self.selection = select(
            *self.options,
            hidden=False if self.options else True,
        )

        self.description = virtue_descriptions[self.name]
        self.label = div(
            input_(
                type="checkbox",
                classes=["form-check-input"],
                checked=self.checked,
                disabled=self.disabled,
                on_click=self.click,
            ),
            self.selection,
            label(
                f"{self.name}:",
                self.description,
                em(f"{self.type}. "),
                strong(f"Cost: {self.cost}"),
            ),
            hidden=self.hidden,
        )

    def click(self, e):
        if e.target.checked:
            CharacterCreation.virtue_points_available.value -= self.cost
            if self.cost < 0:
                CharacterCreation.virtue_points_from_flaws.value -= self.cost
        else:
            CharacterCreation.virtue_points_available.value += self.cost
            if self.cost < 0:
                CharacterCreation.virtue_points_from_flaws.value += self.cost


houses = {
    description.id: House(description.id, description.textContent)
    for description in page["#house_descriptions"][0]["p"]
}

houses["Bonisagus"].selection = select(option("Researcher"), option("Politician"))

virtue_descriptions = {
    description.id: description.textContent
    for description in page["#virtue_descriptions"][0]["p"]
}

hermetic_magus = Virtue(
    name="Hermetic Magus",
    type="Social Status",
    cost=0,
    checked=True,
    disabled=True,
)
the_gift = Virtue(
    name="The Gift",
    type="Special",
    cost=0,
    checked=True,
    disabled=True,
)
heartbeast = Virtue(
    name="Heartbeast", type="Hermetic", cost=1, checked=True, disabled=True, hidden=True
)
the_enigma = Virtue(
    name="The Enigma", type="Hermetic", cost=1, checked=True, disabled=True, hidden=True
)

heartbeast_option = option("Heartbeast", hidden=True)
the_enigma_option = option("The Enigma", hidden=True)
puissant_ability = Virtue(
    name="Puissant Ability",
    type="General",
    cost=1,
    options=[
        option("Magic Theory"),
        option("Intrigue"),
        heartbeast_option,
        the_enigma_option,
    ],
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
    virtue_points_available = OnScreenInt("Virtue Points Available", 0)
    virtue_points_from_flaws = OnScreenInt("Points From Flaws (Max 10)", 0)

    def __init__(self):
        self.house_selection = div(
            p("Which Hermetic House do you hail from?"),
            *(
                p(
                    button(
                        name,
                        type="submit",
                        classes=["btn", "btn-secondary"],
                        on_click=self.house_choice,
                    ),
                    house.selection,
                    house.description,
                )
                for name, house in houses.items()
            ),
            classes=["col"],
        )
        self.virtue_selection = div(
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
                the_enigma.label,
                puissant_ability.label,
            ),
        )

    def start(self):
        main.append(self.house_selection)

    def house_choice(self, e):
        player.house.value = e.target.textContent
        self.house_selection.remove()
        if player.house.value == "Bjornaer":
            heartbeast.label.hidden = False
            heartbeast_option.hidden = False
        elif player.house.value == "Bonisagus":
            puissant_ability.label["input"].checked = True
            if houses["Bonisagus"].selection.value == "Researcher":
                puissant_ability.label["select"].value = "Magic Theory"
            else:
                puissant_ability.label["select"].value = "Intrigue"
            puissant_ability.label["input"].disabled = True
            puissant_ability.label["select"].disabled = True
        elif player.house.value == "Criamon":
            the_enigma.label.hidden = False
            the_enigma_option.hidden = False
        main.append(self.virtue_selection)

    def virtue_choice(self, e):
        self.virtue_selection.remove()
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
