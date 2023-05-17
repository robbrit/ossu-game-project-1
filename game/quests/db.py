"""This module tracks a set of all the quests in the game."""

from typing import (
    Dict,
    Optional,
)

from engine import scripts

from game.quests import base

_quests: Dict[str, base.Quest] = {}


def get(name: str) -> base.Quest:
    """Gets a quest by name."""
    return _quests[name]


def get_state(api: scripts.GameAPI, name: str) -> Optional[base.QuestState]:
    """Gets the state for a specific quest, if any."""
    return api.player_data["quests"].get(name)


def set_state(api: scripts.GameAPI, name: str, state: base.QuestState) -> None:
    """Sets the state for a specific quest."""
    api.player_data["quests"][name] = state


def register(quest: base.Quest) -> None:
    """Registers a quest in the DB."""
    _quests[quest.name] = quest
