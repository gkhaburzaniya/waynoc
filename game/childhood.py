from functools import partial

from .events import Event


class Childhood:

    def __init__(self, player):
        self.events = {
            1/4: [
                Event("You learned to recognize faces.",
                      partial(player.change_intelligence, 1)),
                Event("To look around.",
                      partial(player.change_perception, 1)),
                Event("To lift your head.",
                      partial(player.change_strength, 1)),
                Event("To hold your head steady.",
                      partial(player.change_stamina, 1)),
                Event("To smile at people.",
                      partial(player.change_presence, 1)),
                Event("To coo and babble.",
                      partial(player.change_communication, 1)),
                Event("To suck on your hand.",
                      partial(player.change_dexterity, 1)),
                Event("To swing at dangling toys.",
                      partial(player.change_quickness, 1)),
            ],
            1/2: [
                Event("You learned your name.",
                      partial(player.change_name, "George")),
                Event("You learned to put things in your mouth.",
                      partial(player.change_perception, 1)),
                Event("To sit and roll over.",
                      partial(player.change_strength, 1)),
                Event("To cry in different ways.",
                      partial(player.change_communication, 1)),
                Event("To reach for things.",
                      partial(player.change_dexterity, 1)),
                Event("To crawl.",
                      partial(player.change_quickness, 1)),
            ],
            3/4: [
                Event("You learned to fear strangers.",
                      partial(player.change_intelligence, 1)),
                Event("To look for hidden things",
                      partial(player.change_perception, 1)),
                Event("To stand while holding on to something",
                      partial(player.change_strength, 1)),
                Event("To understand simple sentences, make many sounds and "
                      "simple gestures",
                      partial(player.change_communication, 1)),
                Event("To pick things up and move them between your hands",
                      partial(player.change_dexterity, 1)),
            ],
        }

    def __getitem__(self, item):
        return self.events[item]
