import datetime
import importlib
from typing import (
    Any,
    Callable,
    Optional,
    Protocol,
)

from engine import game_state


GameCallable = Callable[[game_state.GameAPI], None]


def _load_symbol(path: str):
    mod_name, class_name = path.rsplit(".", 1)

    # TODO(rob): Determine if this is insecure.
    mod = importlib.import_module(mod_name)
    return getattr(mod, class_name)


def load_callable(path: str) -> GameCallable:
    """Loads a callable object.

    Note that this doesn't check the arguments/return type.
    """
    obj = _load_symbol(path)
    if not callable(obj):
        raise Exception(f"Object {path} is not callable.")
    return obj


class ScriptOwner(Protocol):
    """Defines an owner for a script."""


class Entity(Protocol):
    """Defines something in the game: a player, a monster, etc."""


class Player(Entity):
    """Represents the player to scripts."""


class Script:
    """Base class for all scripts."""

    def set_api(self, api: game_state.GameAPI):
        """Called after construction to set the API object for the script.

        Can safely be ignored for scripts that don't need it.
        """
        pass

    def on_start(self, owner: ScriptOwner) -> None:
        """Triggered when the owner is loaded for the first time."""
        pass

    def on_tick(self, game_time: datetime.timedelta) -> None:
        """Triggered on every clock tick."""
        pass

    def on_collide(self, owner: ScriptOwner, other: Entity) -> None:
        """Triggered when the owner collides with another entity."""
        pass

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        """Triggered when the player activates the owner.

        Note that this requires the owner to be rectangular."""
        pass

    def on_event(self, event_name: str, data: Any) -> None:
        """Triggered when a custom event is fired."""
        pass


class ObjectScript(Script):
    """Creates a script object that allows pluggable behaviour.

    This is useful for maps that don't want to define an entire class just for something
    simple and instead just want to tie to some function.
    """

    api: Optional[game_state.GameAPI]
    _on_activate: GameCallable
    # TODO(rob): Fill in all the other functions.

    def __init__(self, on_activate: Optional[str]):
        self._on_activate = load_callable(on_activate) if on_activate else self._dummy

    def set_api(self, api: game_state.GameAPI) -> None:
        self.api = api

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        if self._on_activate:
            self._on_activate(self.api)

    def _dummy(self, api: game_state.GameAPI) -> None:
        pass


def load_script_class(path: str) -> Script:
    """Loads a script class at path."""

    cls = _load_symbol(path)
    if not issubclass(cls, Script):
        raise Exception("A script class must inherit from Script.")

    return cls
