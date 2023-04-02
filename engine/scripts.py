import datetime
import importlib
from typing import (
    Any,
    Callable,
    Iterable,
    Optional,
    Protocol,
    Tuple,
)

from arcade import gui

import engine


class GUI(Protocol):
    """A GUI is a set of buttons and images that the user interacts with."""

    def draw(self) -> None:
        """Draws the GUI to the screen."""
        ...

    def set_api(self, api: "GameAPI") -> None:
        """Sets the API for this GUI."""
        ...

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""
        ...


class GameAPI(Protocol):
    """A protocol for how game objects will interact with the engine."""

    def start_game(self) -> None:
        """Starts the game."""
        ...

    def change_region(self, name: str, start_location: str) -> None:
        """Switches the region of the game."""
        ...

    def show_gui(self, gui: GUI) -> None:
        """Shows a GUI."""
        ...

    def create_sprite(
        self,
        spec_name: str,
        name: str,
        start_location: Tuple[int, int],
        script: "Optional[Script]",
    ) -> None:
        """Creates a sprite."""
        ...


GameCallable = Callable[[GameAPI], None]


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

    def set_api(self, api: GameAPI):
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


class SavesAPI:
    """Script mixin to save the API object."""

    api: Optional[GameAPI]

    def __init__(self):
        self.api = None

    def set_api(self, api: GameAPI):
        self.api = api


class ObjectScript(Script):
    """Creates a script object that allows pluggable behaviour.

    This is useful for maps that don't want to define an entire class just for something
    simple and instead just want to tie to some function.
    """

    api: Optional[GameAPI]
    _on_activate: GameCallable
    # TODO(rob): Fill in all the other functions.

    def __init__(self, on_activate: Optional[str]):
        self._on_activate = load_callable(on_activate) if on_activate else self._dummy

    def set_api(self, api: GameAPI) -> None:
        self.api = api

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        if self._on_activate:
            self._on_activate(self.api)

    def _dummy(self, api: GameAPI) -> None:
        pass


def load_script_class(path: str) -> Script:
    """Loads a script class at path."""

    cls = _load_symbol(path)
    if not issubclass(cls, Script):
        raise Exception("A script class must inherit from Script.")

    return cls
