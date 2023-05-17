import dataclasses
from typing import (
    Any,
    Callable,
    Dict,
)

from engine import scripts


@dataclasses.dataclass
class QuestStep:
    """A single step within a quest."""

    description: str


@dataclasses.dataclass
class Quest:
    """Wraps all the information for a quest."""

    name: str
    title: str
    steps: Dict[str, QuestStep]
    initial_step: str
    initial_data: Callable[[scripts.GameAPI], Dict[str, Any]]


@dataclasses.dataclass
class QuestState:
    """Tracks the current state of a quest for the player."""

    current_step: str
    data: Dict[str, Any]
    timestamp: float
