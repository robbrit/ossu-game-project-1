import datetime
import importlib
from typing import (
    Any,
    Callable,
    Protocol,
)

from engine import game_state


GameCallable = Callable[[game_state.GameAPI], None]


def load_callable(path: str) -> GameCallable:
    """Loads a callable object.

    Note that this doesn't actually check if the thing is callable, or checks the
    arguments/return type.
    """
    mod_name, class_name = path.rsplit(".", 1)

    # TODO(rob): Determine if this is insecure.
    mod = importlib.import_module(mod_name)
    return getattr(mod, class_name)


class ScriptOwner(Protocol):
    """Defines an owner for a script."""


class Entity(Protocol):
    """Defines something in the game: a player, a monster, etc."""


class Player(Entity):
    """Represents the player to scripts."""


class Script:
    """Base class for all scripts."""

    def on_start(self, owner: ScriptOwner) -> None:
        pass

    def on_tick(self, game_time: datetime.timedelta) -> None:
        pass

    def on_collide(self, owner: ScriptOwner, other: Entity) -> None:
        pass

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        pass

    def on_event(self, event_name: str, data: Any) -> None:
        pass
