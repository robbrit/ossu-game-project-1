"""This module defines a set of custom event types that are fired by the engine."""

from typing import NamedTuple


SPRITE_REMOVED = "sprite_removed"


class SpriteRemoved(NamedTuple):
    """Event that is fired whenever a sprite is removed from the engine."""

    name: str
