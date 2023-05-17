import dataclasses
import importlib
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Protocol,
    Type,
    Tuple,
)

import arcade
from arcade import gui


class GUI(Protocol):
    """A GUI is a set of buttons and images that the user interacts with."""

    def draw(self) -> None:
        """Draws the GUI to the screen."""

    def set_api(self, api: "GameAPI") -> None:
        """Sets the API for this GUI."""

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""


@dataclasses.dataclass
class KeyPoint:
    """Represents a point of interest in the map."""

    name: str
    location: Tuple[float, float]
    properties: Dict[str, Any]


class Entity(Protocol):
    """Defines something in the game: a player, a monster, etc."""

    @property
    def name(self) -> str:
        """Gets the name of this entity."""


class Player(Protocol):
    """Represents the player to scripts."""


# A type that receives events when they are triggered.
# Note that while this uses `Any`, all custom events defined by the engine use proper
# types and any events defined by games are encouraged to do so as well. An event
# handler may be more specialized than Any.
EventHandler = Callable[[str, Any], None]


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
    ) -> Entity:
        """Creates a sprite."""

    def get_key_points(self, name: Optional[str] = None) -> Iterable[KeyPoint]:
        """Queries for key points within the active region."""

    def get_sprites(self, name: Optional[str] = None) -> Iterable[arcade.Sprite]:
        """Gets all sprites with the given name."""

    def remove_sprite(self, name: str) -> None:
        """Removes a sprite by name."""

    def play_sound(self, name: str) -> None:
        """Plays a sound."""

    def register_handler(self, event_name: str, handler: EventHandler) -> None:
        """Registers an event handler for a custom event."""

    def unregister_handler(self, event_name: str, handler: EventHandler) -> None:
        """Unregisters an event handler."""

    def fire_event(self, event_name: str, data: Any) -> None:
        """Fires an event."""

    @property
    def player_data(self) -> Dict[str, Any]:
        """Gets the player's data."""

    @player_data.setter
    def player_data(self, value: Dict[str, Any]) -> None:
        """Sets the player's data."""

    @property
    def current_time_secs(self) -> float:
        """Gets the current time in seconds."""


GameCallable = Callable[[GameAPI], None]


def load_symbol(path: str) -> Type[Any]:
    """Loads a Python something from a path."""
    mod_name, class_name = path.rsplit(".", 1)

    mod = importlib.import_module(mod_name)
    return getattr(mod, class_name)


def load_callable(path: str) -> GameCallable:
    """Loads a callable object.

    Note that this doesn't check the arguments/return type.
    """
    obj = load_symbol(path)
    if not callable(obj):
        raise ValueError(f"Object {path} is not callable.")
    return obj


class ScriptOwner(Protocol):
    """Defines an owner for a script."""

    @property
    def name(self) -> str:
        """Gets the name of the script owner."""

    @property
    def location(self) -> Tuple[float, float]:
        """Gets the location of the script owner in world coordinates."""

    @property
    def speed(self) -> Tuple[float, float]:
        """Gets the speed of the script owner."""

    @speed.setter
    def speed(self, value: Tuple[float, float]) -> None:
        """Sets the speed of the script owner."""

    @property
    def facing(self) -> Tuple[float, float]:
        """Gets the facing direction of the script owner."""

    @facing.setter
    def facing(self, value: Tuple[float, float]) -> None:
        """Sets the facing direction of the script owner."""

    @property
    def custom_animation(self) -> Optional[str]:
        """Gets the custom animation of the script owner."""

    @custom_animation.setter
    def custom_animation(self, value: Optional[str]) -> None:
        """Sets the custom animation of the script owner."""

    @property
    def is_dying(self) -> bool:
        """Gets the creature is dead or not."""

    @is_dying.setter
    def is_dying(self, value: bool) -> None:
        """Sets the creature is dead or not."""


class Script:
    """Base class for all scripts."""

    _state: Dict[str, Any]

    def __init__(self):
        self._state = {}

    def set_api(self, api: GameAPI):
        """Called after construction to set the API object for the script.

        Can safely be ignored for scripts that don't need it.
        """

    def set_owner(self, owner: ScriptOwner):
        """Sets the owner of this script."""

    def on_start(self, owner: ScriptOwner) -> None:
        """Triggered when the owner is loaded for the first time."""

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Triggered on every clock tick."""

    def on_collide(self, owner: ScriptOwner, other: Entity) -> None:
        """Triggered when the owner collides with another entity."""

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        """Triggered when the player activates the owner.

        Note that this requires the owner to be rectangular."""

    def on_hit(self, owner: ScriptOwner, player: Player) -> None:
        """Triggered when the player hit the owner."""

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

    api: Optional[GameAPI] = None

    def set_api(self, api: GameAPI):
        """Sets the API for this script."""
        self.api = api


class SavesOwner:
    """Script mixin to save the owner object."""

    owner: Optional[ScriptOwner] = None

    def set_owner(self, owner: ScriptOwner):
        """Sets the owner for this script."""
        self.owner = owner


class ObjectScript(Script):
    """Creates a script object that allows pluggable behaviour.

    This is useful for maps that don't want to define an entire class just for something
    simple and instead just want to tie to some function.
    """

    api: GameAPI
    _on_activate: GameCallable
    _on_activate_args: Dict[str, Any]
    _on_hit: GameCallable
    _on_hit_args: Dict[str, Any]
    _on_collide: GameCallable
    _on_collide_args: Dict[str, Any]
    _on_start: GameCallable
    _on_start_args: Dict[str, Any]
    _on_tick: GameCallable
    _on_tick_args: Dict[str, Any]

    def __init__(
        self,
        api: GameAPI,
        on_activate: Optional[str],
        on_activate_args: Dict[str, Any],
        on_hit: Optional[str],
        on_hit_args: Dict[str, Any],
        on_collide: Optional[str],
        on_collide_args: Dict[str, Any],
        on_start: Optional[str],
        on_start_args: Dict[str, Any],
        on_tick: Optional[str],
        on_tick_args: Dict[str, Any],
    ):
        super().__init__()
        self.api = api
        self._on_activate = load_callable(on_activate) if on_activate else self._dummy
        self._on_activate_args = on_activate_args
        self._on_hit = load_callable(on_hit) if on_hit else self._dummy
        self._on_hit_args = on_hit_args
        self._on_collide = load_callable(on_collide) if on_collide else self._dummy
        self._on_collide_args = on_collide_args
        self._on_start = load_callable(on_start) if on_start else self._dummy
        self._on_start_args = on_start_args
        self._on_tick = load_callable(on_tick) if on_tick else self._dummy
        self._on_tick_args = on_tick_args

    def set_api(self, api: GameAPI) -> None:
        self.api = api

    def on_start(self, owner: ScriptOwner) -> None:
        self._on_start(self.api, **self._on_start_args)

    def on_tick(self, game_time: float, delta_time: float) -> None:
        self._on_tick(self.api, **self._on_tick_args)

    def on_activate(self, owner: ScriptOwner, player: Player) -> None:
        self._on_activate(self.api, **self._on_activate_args)

    def on_hit(self, owner: ScriptOwner, player: Player) -> None:
        self._on_hit(self.api, **self._on_hit_args)

    def on_collide(self, owner: ScriptOwner, other: Entity) -> None:
        self._on_collide(self.api, **self._on_collide_args)

    def _dummy(self, api: GameAPI) -> None:
        pass


def load_script_class(path: str) -> Type[Script]:
    """Loads a script class at path."""

    cls = load_symbol(path)
    if not issubclass(cls, Script):
        raise TypeError("A script class must inherit from Script.")

    return cls


def extract_script_args(prefix: str, properties: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts a set of arguments from a dict that has a certain prefix.

    The prefix is stripped from the keys in the result.
    """
    return {
        key.removeprefix(prefix): value
        for key, value in properties.items()
        if key.startswith(prefix)
    }
