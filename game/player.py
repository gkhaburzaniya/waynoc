from dataclasses import dataclass

from .events import EventText
from .childhood import Childhood


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
