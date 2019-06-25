from dataclasses import dataclass
from functools import partial


@dataclass(frozen=True)
class Event:
    flavor: str
    effect: partial


@dataclass(frozen=True)
class EventText:
    flavor_text: str
    effect_text: str
