""" Game logic goes here """

from dataclasses import dataclass


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
        return flavor_text.get(self.age)


player = Player()


def advance():
    player.age += 0.25


def restart():
    global player
    player = Player()


flavor_text = {
    0: "You are born\n",
    0.25: "You learned to smile.\n"
          "To bring your hands to your mouth and suck on your hand.\n"
          "To look around.\n"
          "To coo.\n"
          "To move your head.\n"
          "To recognize faces.\n"}
