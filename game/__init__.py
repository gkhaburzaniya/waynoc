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
        return '\n'.join(flavor_text.get(self.age, []))


player = Player()


def advance():
    player.age += 0.25


def restart():
    global player
    player = Player()


flavor_text = {
    0: ["You are born"],
    1/4: ["You learned to smile. <b>+1 Presence</b>",
          "To suck on your hand. <b>+1 Dexterity</b>",
          "To look around. <b>+1 Perception</b>",
          "To coo. <b>+1 Communication</b>",
          "To move your head. <b>+1 Strength</b>",
          "To recognize faces. <b>+1 Intelligence</b>"]}
