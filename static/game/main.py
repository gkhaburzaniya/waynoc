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


class Ability:

    def __init__(self, name, hidden=False):
        self.option_locations = []
        self.name = name
        self.hidden = hidden

    def option(self):
        new_option = option(self.name, hidden=self.hidden)
        self.option_locations.append(new_option)
        return new_option

    @property
    def hidden(self):
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = value
        for option_loc in self.option_locations:
            option_loc.hidden = value


@dataclass
class Virtue:
    name: str
    type: str
    cost: int
    disabled: bool = False
    hidden: bool = False
    options: list = field(default_factory=list)
    only_one: str = ""

    def __post_init__(self):
        self.selection = select(
            *self.options,
            hidden=False if self.options else True,
        )

        self.description = virtue_descriptions[self.name]
        self.label = div(
            label(
                input_(
                    name=self.only_one,
                    type="checkbox",
                    classes=["form-check-input"],
                    disabled=self.disabled,
                    on_click=self.click,
                ),
                self.selection,
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
        if self.only_one:
            page[f"[name='{self.only_one}']"].disabled = e.target.checked
            e.target.disabled = False


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
    disabled=True,
)
the_gift = Virtue(
    name="The Gift",
    type="Special",
    cost=0,
    disabled=True,
)
heartbeast_virtue = Virtue(
    name="Heartbeast", type="Hermetic", cost=1, disabled=True, hidden=True
)
the_enigma_virtue = Virtue(
    name="The Enigma", type="Hermetic", cost=1, disabled=True, hidden=True
)

magic_theory = Ability("Magic Theory")
intrigue = Ability("Intrigue")
heartbeast_ability = Ability("Heartbeast", hidden=True)
the_enigma_ability = Ability("The Enigma", hidden=True)


def ability_options():
    return [
        magic_theory.option(),
        intrigue.option(),
        heartbeast_ability.option(),
        the_enigma_ability.option(),
    ]


affinity_with_ability = Virtue(
    name="Affinity with Ability", type="General", cost=1, options=ability_options()
)
puissant_ability = Virtue(
    name="Puissant Ability",
    type="General",
    cost=1,
    options=ability_options(),
)

elemental_magic = Virtue(
    name="Elemental Magic", type="Hermetic", cost=3, only_one="Major Hermetic Virtue"
)
flawless_magic = Virtue(
    name="Flawless Magic", type="Hermetic", cost=3, only_one="Major Hermetic Virtue"
)
flexible_formulaic_magic = Virtue(
    name="Flexible Formulaic Magic",
    type="Hermetic",
    cost=3,
    only_one="Major Hermetic Virtue",
)

deficient_technique = Virtue(
    name="Deficient Technique",
    type="Hermetic",
    cost=-3,
    options=[
        option("Creo"),
        option("Intellego"),
        option("Muto"),
        option("Perdo"),
        option("Rego"),
    ],
)
deft_form = Virtue(
    name="Deft Form",
    type="Hermetic",
    cost=1,
    options=[
        option("Animal"),
        option("Aquam"),
        option("Auram"),
        option("Corpus"),
        option("Herbam"),
        option("Ignem"),
        option("Imaginem"),
        option("Mentem"),
        option("Terram"),
        option("Vim"),
    ],
)
careless_sorcerer = Virtue(name="Careless Sorcerer", type="Hermetic", cost=-1)
clumsy_magic = Virtue(name="Clumsy Magic", type="Hermetic", cost=-1)
adept_laboratory_student = Virtue(
    name="Adept Laboratory Student", type="Hermetic", cost=1
)
giant_blood = Virtue(name="Giant Blood", type="General", cost=3)
ways_of_the_land = Virtue(
    name="Ways of the Land",
    type="General",
    cost=3,
    options=[option("Forest"), option("Mountain"), option("Steppe"), option("Town")],
)
martial_block = Virtue(name="Martial Block", type="General", cost=-1)
afflicted_tongue = Virtue(name="Afflicted Tongue", type="General", cost=-1)
arthritis = Virtue(name="Arthritis", type="General", cost=-1)
blind = Virtue(name="Blind", type="General", cost=-3)
crippled = Virtue(name="Crippled", type="General", cost=-3)
deaf = Virtue(name="Deaf", type="General", cost=-3)


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
                heartbeast_virtue.label,
                the_enigma_virtue.label,
                puissant_ability.label,
                elemental_magic.label,
                flawless_magic.label,
                flexible_formulaic_magic.label,
                deficient_technique.label,
                careless_sorcerer.label,
                clumsy_magic.label,
                adept_laboratory_student.label,
                affinity_with_ability.label,
                deft_form.label,
                giant_blood.label,
                ways_of_the_land.label,
                martial_block.label,
                afflicted_tongue.label,
                arthritis.label,
                blind.label,
                crippled.label,
                deaf.label,
            ),
        )

    def start(self):
        main.append(self.house_selection)

    def house_choice(self, e):
        player.house.value = e.target.textContent
        self.house_selection.remove()
        the_gift.label["input"].checked = True
        hermetic_magus.label["input"].checked = True
        if player.house.value == "Bjornaer":
            heartbeast_virtue.label["input"].checked = True
            heartbeast_virtue.label.hidden = False
            heartbeast_ability.hidden = False
        elif player.house.value == "Bonisagus":
            puissant_ability.label["input"].checked = True
            if houses["Bonisagus"].selection.value == "Researcher":
                puissant_ability.label["select"].value = "Magic Theory"
            else:
                puissant_ability.label["select"].value = "Intrigue"
            puissant_ability.label["input"].disabled = True
            puissant_ability.label["select"].disabled = True
        elif player.house.value == "Criamon":
            the_enigma_virtue.label["input"].checked = True
            the_enigma_virtue.label.hidden = False
            the_enigma_ability.hidden = False
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
