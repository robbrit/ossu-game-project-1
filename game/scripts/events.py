"""Defines a number of events used in the game."""

from typing import (
    NamedTuple,
)

CREATURE_KILLED = "creature_killed"


class CreatureKilled(NamedTuple):
    """Event fired when a creature is killed."""

    creature_type: str
