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

    @property
    def value(self):
        return self._value.textContent

    @value.setter
    def value(self, value):
        self._value.textContent = value

    @property
    def element(self):
        self._value = span(self.value)
        return span(
            f" {self.short_name}: ", self._value, " ", classes=["text-monospace"]
        )


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


class Ability(OnScreenInt):

    def __init__(self, short_name, hidden=False):
        self.option_locations = []
        self.hidden = hidden
        super().__init__(short_name, 0)

    def __hash__(self):
        return hash(self.short_name)

    def __eq__(self, other):
        return self.short_name == other

    def __repr__(self):
        return f"{self.short_name}: {self.value}"

    def option(self):
        new_option = option(self.short_name, hidden=self.hidden)
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


athletics = Ability("Athletics")
artes_liberales = Ability("Artes Liberales")
awareness = Ability("Awareness")
brawl = Ability("Brawl")
guile = Ability("Guile")
intrigue = Ability("Intrigue")

# Languages
english = Ability("English")
latin = Ability("Latin")
mandarin = Ability("Mandarin")
spanish = Ability("Spanish")

# Lores
china_lore = Ability("China Lore")
mexico_lore = Ability("Mexico Lore")
usa_lore = Ability("USA Lore")

stealth = Ability("Stealth")
survival = Ability("Survival")
swim = Ability("Swim")

# Magic
magic_theory = Ability("Magic Theory")
parma_magica = Ability("Parma Magica", hidden=True)

heartbeast_ability = Ability("Heartbeast", hidden=True)
the_enigma_ability = Ability("The Enigma", hidden=True)

ability_list = [
    athletics,
    artes_liberales,
    awareness,
    brawl,
    guile,
    intrigue,
    english,
    latin,
    mandarin,
    spanish,
    china_lore,
    mexico_lore,
    usa_lore,
    magic_theory,
    stealth,
    survival,
    swim,
    heartbeast_ability,
    the_enigma_ability,
    parma_magica,
]

# Arts - Techniques
creo = Ability("Creo")
intellego = Ability("Intellego")
muto = Ability("Muto")
perdo = Ability("Perdo")
rego = Ability("Rego")

techinque_list = [creo, intellego, muto, perdo, rego]

# Arts - Form

animal = Ability("Animal")
aquam = Ability("Aquam")
auram = Ability("Auram")
corpus = Ability("Corpus")
herbam = Ability("Herbam")
ignem = Ability("Ignem")
imaginem = Ability("Imaginem")
mentem = Ability("Mentem")
terram = Ability("Terram")
vim = Ability("Vim")

form_list = [animal, aquam, auram, corpus, herbam, ignem, imaginem, mentem, terram, vim]

arts_list = techinque_list + form_list


def ability_options():
    return [ability.option() for ability in ability_list]


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
                    onclick=self.click,
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
    options=[technique.option() for technique in techinque_list],
)
deft_form = Virtue(
    name="Deft Form",
    type="Hermetic",
    cost=1,
    options=[form.option() for form in form_list],
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

all_virtues = [
    hermetic_magus,
    the_gift,
    heartbeast_virtue,
    the_enigma_virtue,
    affinity_with_ability,
    puissant_ability,
    elemental_magic,
    flawless_magic,
    flexible_formulaic_magic,
    deficient_technique,
    deft_form,
    clumsy_magic,
    careless_sorcerer,
    adept_laboratory_student,
    giant_blood,
    ways_of_the_land,
    martial_block,
    afflicted_tongue,
    arthritis,
    blind,
    crippled,
    deaf,
]


class Player:

    def __init__(self):
        self.intelligence = Characteristic("Int", 0)
        self.perception = Characteristic("Per", 0)
        self.strength = Characteristic("Str", 0)
        self.stamina = Characteristic("Sta", 0)
        self.presence = Characteristic("Prs", 0)
        self.communication = Characteristic("Com", 0)
        self.dexterity = Characteristic("Dex", 0)
        self.quickness = Characteristic("Qik", 0)

        self.name = OnScreenValue("Name", "")
        self.age = Age("Age", 0)
        self.house = OnScreenValue("House", "")
        self.virtues = []
        self.abilities = {ability: ability for ability in ability_list}
        self.arts = {art: art for art in arts_list}

        self.text = [EventText("You are born", "")]

    def change_name(self, new_name):
        self.name.value = new_name
        self.effect_text = f"Your name is {new_name}"
        return self


def start(_):
    start_button.remove()
    custom_character_button.remove()
    player.childhood = Childhood(player)
    main.append(new_board())


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
    characteristic_points = OnScreenInt("Points", 7)
    experience_points = OnScreenInt("XP", 75)
    name_input = div(input_(value="George"))
    language_input = div(
        label(input_(type="radio", name="language", value="English"), "English"),
        label(
            input_(
                type="radio",
                name="language",
                value="Mandarin",
                checked=True,
            ),
            "Mandarin",
        ),
        label(input_(type="radio", name="language", value="Spanish"), "Spanish"),
    )
    birthplace_input = div(
        label(
            input_(type="radio", name="birthplace", value="China", checked=True),
            "China",
        ),
        label(input_(type="radio", name="birthplace", value="USA"), "USA"),
        label(input_(type="radio", name="birthplace", value="Mexico"), "Mexico"),
    )
    childhood_input = div(
        label(
            input_(type="radio", name="type", value="Athletic", checked=True),
            "Athletic",
        ),
        label(input_(type="radio", name="type", value="Exploring"), "Exploring"),
        label(input_(type="radio", name="type", value="Mischievous"), "Mischievous"),
    )

    def __init__(self):
        self.house_selection = div(
            p("Which Hermetic House do you hail from?"),
            *(
                p(
                    button(
                        name,
                        type="submit",
                        classes=["btn", "btn-secondary"],
                        onclick=self.house_choice,
                    ),
                    house.selection,
                    house.description,
                )
                for name, house in houses.items()
            ),
            classes=["col"],
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
            heartbeast_ability.value = 1
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
            the_enigma_ability.value = 1

        self.virtue_selection = div(
            "What are your virtues and flaws?",
            table(
                tbody(
                    tr(
                        td(h5(self.virtue_points_available.element)),
                        td(h5(self.virtue_points_from_flaws.element)),
                    )
                ),
                classes=["table", "table-borderless", "table-sm"],
            ),
            div(
                button(
                    "Next",
                    type="submit",
                    classes=["btn", "btn-secondary"],
                    onclick=self.virtue_choice,
                ),
                *(virtue.label for virtue in all_virtues),
            ),
        )

        main.append(self.virtue_selection)

    def virtue_choice(self, _):
        self.virtue_selection.remove()
        player.virtues = [
            virtue for virtue in all_virtues if virtue.label["input"][0].checked
        ]

        self.characteristic_selection = div(
            table(
                tbody(
                    tr(
                        td(h5(self.characteristic_points.element)),
                    )
                ),
                classes=["table", "table-borderless", "table-sm"],
            ),
            "What are your characteristics?",
            characteristic_display(),
            button(
                "Next",
                type="submit",
                classes=["btn", "btn-secondary"],
                onclick=self.characteristic_choice,
            ),
        )

        main.append(self.characteristic_selection)
        self.characteristic_selection["button"].hidden = False
        magic_theory.hidden = True
        heartbeast_ability.hidden = True
        the_enigma_ability.hidden = True

    def characteristic_choice(self, _):
        self.characteristic_selection.remove()
        self.early_childhood_selection = div(
            div(
                "What is your name?",
                self.name_input,
            ),
            div("What is your primary language?", self.language_input),
            div(
                "Where did you grow up?",
                self.birthplace_input,
            ),
            div(
                "What kind of childhood did you have?",
                self.childhood_input,
            ),
            button(
                "Next",
                type="submit",
                classes=["btn", "btn-secondary"],
                onclick=self.early_childhood_choice,
            ),
        )
        main.append(self.early_childhood_selection)

    def early_childhood_choice(self, _):
        self.early_childhood_selection.remove()
        player.name.value = self.name_input["input"][0].value
        language = self.language_input["input:checked"][0].value
        birthplace = self.birthplace_input["input:checked"][0].value
        childhood = self.childhood_input["input:checked"][0].value
        player.age.value = 5
        player.abilities[language].value = 5
        if childhood == "Athletic":
            player.abilities[athletics].value = 2
            player.abilities[brawl].value = 2
            player.abilities[swim].value = 2
        elif childhood == "Exploring":
            player.abilities[f"{birthplace} Lore"].value = 2
            player.abilities[athletics].value = 1
            player.abilities[awareness].value = 1
            player.abilities[stealth].value = 1
            player.abilities[survival].value = 1
        elif childhood == "Mischievous":
            player.abilities[brawl].value = 2
            player.abilities[guile].value = 2
            player.abilities[stealth].value = 2

        self.next_button = button(
            "Next",
            type="submit",
            classes=["btn", "btn-secondary"],
            onclick=self.later_life_choice,
        )

        self.abilities_body = tbody(
            *(
                single_ability_display(ability)
                for ability in ability_list
                if not ability.hidden
            )
        )
        self.intro_text = span("What did you learn between ages 5 and 10?")

        self.tables_div = div(
            div(
                table(
                    self.abilities_body,
                    classes=[
                        "table",
                        "table-striped",
                        "table-borderless",
                        "table-hover",
                        "table-sm",
                    ],
                ),
                classes=["col-4", "col-md-3"],
            ),
            classes=["row"],
        )

        self.later_life_selection = div(
            self.intro_text,
            div(self.next_button),
            table(
                tbody(tr(td(h5(self.experience_points.element)))),
                classes=["table", "table-borderless", "table-sm"],
            ),
            self.tables_div,
        )
        main.append(self.later_life_selection)

    def later_life_choice(self, _):
        player.age.value += 5
        parma_magica.value = 1
        magic_theory.value = 1
        magic_theory.hidden = False
        self.abilities_body.append(single_ability_display(magic_theory))
        for button_ in self.abilities_body["button"]:
            if button_.textContent == "-":
                button_.disabled = True
        self.experience_points.value = 230
        if latin.value < 1:
            latin.value = 1
            self.experience_points.value -= 5
        self.intro_text.textContent = (
            "What did you learn in your apprenticeship? Recommended to have at least "
            "Magic Theory 3, Artes Liberales 4, and Latin 5"
        )
        self.next_button.onclick = self.apprenticeship_choice
        self.tables_div.append(
            div(
                table(
                    tbody(*(single_art_display(art) for art in arts_list)),
                    classes=[
                        "table",
                        "table-striped",
                        "table-borderless",
                        "table-hover",
                        "table-sm",
                    ],
                ),
                classes=["col-4", "col-md-3", "offset-md-3"],
            ),
        )

    def apprenticeship_choice(self, e):
        self.later_life_selection.remove()
        player.age.value += 15
        start(e)
        main.append(div(ability_list))
        main.append(div(arts_list))


page["#loading"][0].remove()
main = page["main"][0]
start_button = button(
    "Start", type="submit", classes=["btn", "btn-secondary"], onclick=start
)
custom_character_button = button(
    "Custom Character",
    type="submit",
    classes=["btn", "btn-secondary"],
    onclick=custom_character,
)

events = div()

player = Player()


def single_characteristic_display(characteristic):
    def decrease_characteristic(_):
        characteristic.value -= 1
        if characteristic.value == 2:
            CharacterCreation.characteristic_points.value += 3
            plus_button.disabled = False
        elif characteristic.value in {1, -2}:
            CharacterCreation.characteristic_points.value += 2
        elif characteristic.value in {0, -1}:
            CharacterCreation.characteristic_points.value += 1
        elif characteristic.value == -3:
            minus_button.disabled = True
            CharacterCreation.characteristic_points.value += 3

    def increase_characteristic(_):
        characteristic.value += 1
        if characteristic.value == -2:
            CharacterCreation.characteristic_points.value -= 3
            minus_button.disabled = False
        elif characteristic.value in {-1, 2}:
            CharacterCreation.characteristic_points.value -= 2
        elif characteristic.value in {0, 1}:
            CharacterCreation.characteristic_points.value -= 1
        elif characteristic.value == 3:
            plus_button.disabled = True
            CharacterCreation.characteristic_points.value -= 3

    minus_button = button(
        "-",
        hidden=True,
        classes=["btn", "btn-secondary", "btn-sm"],
        onclick=decrease_characteristic,
    )
    plus_button = button(
        "+",
        hidden=True,
        classes=["btn", "btn-secondary", "btn-sm", "float-right"],
        onclick=increase_characteristic,
    )
    return tr(
        td(
            minus_button,
            characteristic.element,
            plus_button,
        )
    )


def single_ability_display(ability):
    def decrease_ability(_):
        ability.value -= 1
        plus_button.disabled = False
        CharacterCreation.experience_points.value += (ability.value + 1) * 5
        if ability.value == 0:
            minus_button.disabled = True

    def increase_ability(_):
        ability.value += 1
        minus_button.disabled = False
        CharacterCreation.experience_points.value -= ability.value * 5
        if ability.value == 10:
            plus_button.disabled = True

    minus_button = button(
        "-",
        classes=["btn", "btn-secondary", "btn-sm"],
        disabled=True,
        onclick=decrease_ability,
    )
    plus_button = button(
        "+",
        classes=["btn", "btn-secondary", "btn-sm", "float-right"],
        onclick=increase_ability,
    )
    return tr(
        td(
            minus_button,
            ability.element,
            plus_button,
        )
    )


def single_art_display(art):
    def decrease_art(_):
        art.value -= 1
        plus_button.disabled = False
        CharacterCreation.experience_points.value += art.value + 1
        if art.value == 0:
            minus_button.disabled = True

    def increase_art(_):
        art.value += 1
        minus_button.disabled = False
        CharacterCreation.experience_points.value -= art.value
        if art.value == 10:
            plus_button.disabled = True

    minus_button = button(
        "-",
        classes=["btn", "btn-secondary", "btn-sm"],
        disabled=True,
        onclick=decrease_art,
    )
    plus_button = button(
        "+",
        classes=["btn", "btn-secondary", "btn-sm", "float-right"],
        onclick=increase_art,
    )
    return tr(
        td(
            minus_button,
            art.element,
            plus_button,
        )
    )


def characteristic_display():
    return div(
        table(
            tbody(
                single_characteristic_display(player.intelligence),
                single_characteristic_display(player.perception),
                single_characteristic_display(player.strength),
                single_characteristic_display(player.stamina),
                single_characteristic_display(player.presence),
                single_characteristic_display(player.communication),
                single_characteristic_display(player.dexterity),
                single_characteristic_display(player.quickness),
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
    )


def new_board():
    return div(
        characteristic_display(),
        div(
            button(
                "Next Season",
                type="submit",
                classes=["btn", "btn-secondary"],
                onclick=advance,
            ),
            button(
                "Restart",
                type="submit",
                classes=["btn", "btn-secondary"],
                onclick=restart,
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


main.append(start_button, custom_character_button)


def update_state():
    events.innerHTML = ""
    for event in player.text:
        events.innerHTML += event.flavor_text + "<br>"
        events.innerHTML += "<b>" + event.effect_text + "</b><br>"
