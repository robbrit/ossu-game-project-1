import datetime
import importlib
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Protocol,
    Type,
    Tuple,
)

from arcade import gui


class GUI(Protocol):
    """A GUI is a set of buttons and images that the user interacts with."""

    def draw(self) -> None:
        """Draws the GUI to the screen."""

    def set_api(self, api: "GameAPI") -> None:
        """Sets the API for this GUI."""

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""


class GameAPI(Protocol):
    """A protocol for how game objects will interact with the engine."""

    def start_game(self) -> None:
        """Starts the game."""

    def change_region(self, name: str, start_location: str) -> None:
        """Switches the region of the game."""

    def show_gui(self, _gui: GUI) -> None:
        """Shows a GUI."""

    def create_sprite(
        self,
        spec_name: str,
        name: str,
        start_location: Tuple[float, float],
        script: "Optional[Script]",
    ) -> None:
        """Creates a sprite."""


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
        raise ValueError(f"Object {path} is not callable.")
    return obj


class ScriptOwner(Protocol):
    """Defines an owner for a script."""


class Entity(Protocol):
    """Defines something in the game: a player, a monster, etc."""


class Player(Protocol):
    """Represents the player to scripts."""


class Script:
    """Base class for all scripts."""

    _state: Dict[str, Any]

    def set_api(self, api: GameAPI):
        """Called after construction to set the API object for the script.

        Can safely be ignored for scripts that don't need it.
        """

    def on_start(self, owner: ScriptOwner) -> None:
        """Triggered when the owner is loaded for the first time."""

    def on_tick(self, game_time: datetime.timedelta) -> None:
        """Triggered on every clock tick."""

    def on_collide(self, owner: ScriptOwner, other: Entity) -> None:
        """Triggered when the owner collides with another entity."""

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        """Triggered when the player activates the owner.

        Note that this requires the owner to be rectangular."""

    def on_event(self, event_name: str, data: Any) -> None:
        """Triggered when a custom event is fired."""

    @property
    def state(self) -> Dict[str, Any]:
        """Gets the persistable state of this script."""
        return self._state

    @state.setter
    def state(self, value: Dict[str, Any]) -> None:
        """Sets the persistable state of this script."""
        self._state = value


class SavesAPI:
    """Script mixin to save the API object."""

    api: Optional[GameAPI]

    def __init__(self):
        self.api = None

    def set_api(self, api: GameAPI):
        """Sets the API for this script."""
        self.api = api


class ObjectScript(Script):
    """Creates a script object that allows pluggable behaviour.

    This is useful for maps that don't want to define an entire class just for something
    simple and instead just want to tie to some function.
    """

    api: GameAPI
    _on_activate: GameCallable
    _on_activate_args: Dict[str, Any]
    _on_collide: GameCallable
    _on_collide_args: Dict[str, Any]
    _on_start: GameCallable
    _on_start_args: Dict[str, Any]

    # TODO(rob): Fill in all the other functions.

    def __init__(
        self,
        api: GameAPI,
        on_activate: Optional[str],
        on_activate_args: Dict[str, Any],
        on_collide: Optional[str],
        on_collide_args: Dict[str, Any],
        on_start: Optional[str],
        on_start_args: Dict[str, Any],
    ):
        self.api = api
        self._on_activate = load_callable(on_activate) if on_activate else self._dummy
        self._on_activate_args = on_activate_args
        self._on_collide = load_callable(on_collide) if on_collide else self._dummy
        self._on_collide_args = on_collide_args
        self._on_start = load_callable(on_start) if on_start else self._dummy
        self._on_start_args = on_start_args

    def set_api(self, api: GameAPI) -> None:
        self.api = api

    def on_start(self, owner: ScriptOwner) -> None:
        self._on_start(self.api, **self._on_start_args)

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        self._on_activate(self.api, **self._on_activate_args)

    def on_collide(self, owner: ScriptOwner, other: Entity) -> None:
        self._on_collide(self.api, **self._on_collide_args)

    def _dummy(self, api: GameAPI) -> None:
        pass


def load_script_class(path: str) -> Type[Script]:
    """Loads a script class at path."""

    cls = _load_symbol(path)
    if not issubclass(cls, Script):
        raise TypeError("A script class must inherit from Script.")

    return cls
