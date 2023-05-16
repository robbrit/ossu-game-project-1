"""This module tracks a set of all the quests in the game."""

from typing import (
    Dict,
)

from game.quests import base

_quests: Dict[str, base.Quest] = {}


def get(name: str) -> base.Quest:
    """Gets a quest by name."""
    return _quests[name]
