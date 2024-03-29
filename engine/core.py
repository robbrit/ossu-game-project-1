from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Optional,
    Tuple,
)

import arcade
import arcade.tilemap

from engine import (
    event_manager,
    events,
    game_state,
    scripts,
    spec,
)
from engine.gui import game_state as gui_game_state
from engine.ingame import game_state as ingame_state
from engine.model import world

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "OSSU Game Project"


class GameNotInitializedError(Exception):
    """Raised when functions are called before the game was properly initialized."""


class Core(arcade.Window):
    """
    Main application class, wraps everything.
    Implements scripts.GameAPI.

    The game uses an MVC pattern:
    * Model - capture the state of the world in the game: players, regions, enemies,
      etc.
    * Views - handle rendering anything.
    * Controllers - handles interacting with the user.

    There's only one model, but the views and controllers are wrapped by GameState
    objects. The game can be in one of two possible states:
    * In a GUI - the model does not update, we render some sort of GUI, and all controls
      go to manipulating the GUI.
    * In the game - the model updates and all controls go to managing the character.
    """

    current_state: Optional[game_state.GameState]
    gui_state: gui_game_state.GuiState
    ingame_state: Optional[ingame_state.InGameState]

    world: Optional[world.World]
    initial_gui: scripts.GUI
    ingame_gui: Optional[scripts.GUI]
    menu_gui: scripts.GUI
    initial_player_state: Dict[str, Any]
    _spec: spec.GameSpec

    _sounds: Dict[str, arcade.Sound]
    _events: event_manager.EventManager

    def __init__(
        self,
        initial_gui: Callable[[scripts.GameAPI], scripts.GUI],
        menu_gui: Callable[[scripts.GameAPI], scripts.GUI],
        game_spec: spec.GameSpec,
        initial_player_state: Dict[str, Any],
        ingame_gui: Optional[Callable[[scripts.GameAPI], scripts.GUI]] = None,
    ):
        """Constructor.

        Args:
            initial_gui: The GUI screen to show when the game starts.
        """
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
        )

        self._spec = game_spec
        self.world = None
        self.initial_gui = initial_gui(self)
        self.ingame_gui = ingame_gui(self) if ingame_gui else None
        self.menu_gui = menu_gui(self)
        self.initial_player_state = initial_player_state
        self.gui_state = gui_game_state.GuiState(self, self.initial_gui)
        self.ingame_state = None
        self.current_state = None

        self._sounds = {}
        for name, sound_spec in game_spec.sounds.items():
            sound = arcade.load_sound(sound_spec.path, streaming=sound_spec.stream)
            if sound is None:
                raise ValueError(f"Unable to load sound '{name}'")

            self._sounds[name] = sound

        self._events = event_manager.EventManager()

    def setup(self) -> None:
        """Resets the game state."""
        self.gui_state.setup()

    def start_game(self) -> None:
        """Switches to the "in game" state."""
        if self.world is None:
            self.world = world.World(self, self._spec, self.initial_player_state)

        if self.ingame_state is None:
            self.ingame_state = ingame_state.InGameState(
                self.world,
                (self.width, self.height),
                self.ingame_gui,
                self.menu_gui,
                self,
            )

        self.current_state = self.ingame_state

    def change_region(self, name: str, start_location: str) -> None:
        """Changes the region of the game."""
        if self.world is None:
            raise GameNotInitializedError()

        self.world.load_region(name, start_location)

    def show_gui(self, gui: scripts.GUI) -> None:
        """Switches to the "GUI" state, and displays a certain GUI."""
        self.gui_state.set_gui(gui)
        self.current_state = self.gui_state

    def create_sprite(
        self,
        spec_name: str,
        name: str,
        start_location: Tuple[int, int],
        script: Optional[scripts.Script],
    ) -> scripts.Entity:
        """Creates a sprite."""
        if self.world is None:
            raise GameNotInitializedError()

        _spec = self._spec.sprites[spec_name]
        return self.world.create_sprite(_spec, name, start_location, script)

    def get_key_points(self, name: Optional[str] = None) -> Iterable[scripts.KeyPoint]:
        """Queries for key points in the current region."""
        if self.world is None:
            raise GameNotInitializedError()

        return self.world.get_key_points(name)

    def get_sprites(self, name: Optional[str] = None) -> Iterable[arcade.Sprite]:
        """Gets all sprites with the given name."""
        if self.world is None:
            raise GameNotInitializedError()

        return self.world.get_sprites(name)

    def remove_sprite(self, name: str) -> None:
        """Removes a sprite by name."""
        self.fire_event(events.SPRITE_REMOVED, events.SpriteRemoved(name))

    def play_sound(self, name: str) -> None:
        """Plays a sound."""
        self._sounds[name].play()

    def register_handler(self, event_name: str, handler: scripts.EventHandler) -> None:
        """Registers an event handler for a custom event."""
        self._events.register_handler(event_name, handler)

    def unregister_handler(
        self,
        event_name: str,
        handler: scripts.EventHandler,
    ) -> None:
        """Unregisters an event handler."""
        self._events.unregister_handler(event_name, handler)

    def fire_event(self, event_name: str, data: Any) -> None:
        """Fires an event."""
        self._events.fire_event(event_name, data)

    def clear_events(self) -> None:
        """Clears all events."""
        self._events.clear_events()

    @property
    def player_data(self) -> Dict[str, Any]:
        """Gets the player's data."""
        if self.world is None:
            raise GameNotInitializedError()

        return self.world.player_sprite.data

    @player_data.setter
    def player_data(self, value: Dict[str, Any]):
        """Sets the player's data."""
        if self.world is None:
            raise GameNotInitializedError()

        self.world.player_sprite.data = value

    @property
    def current_time_secs(self) -> float:
        """Gets the current time in seconds."""
        if self.world is None:
            raise GameNotInitializedError()

        return self.world.game_time_sec

    def run(self):
        """Runs the game."""
        self.setup()
        self.show_gui(self.initial_gui)
        arcade.run()

    ############################################################################
    # The rest of the methods are there to tie into Arcade's input and rendering
    # system. For the most part they are just delegates to the appropriate
    # object.
    ############################################################################

    def on_draw(self) -> None:
        """Renders the game."""
        if self.current_state is None:
            raise GameNotInitializedError()

        self.clear()
        self.current_state.view.on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handles incoming key presses."""
        if self.current_state is None:
            raise GameNotInitializedError()

        self.current_state.controller.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handles incoming key releases."""
        if self.current_state is None:
            raise GameNotInitializedError()

        self.current_state.controller.on_key_release(symbol, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handles mouse movement."""
        if self.current_state is None:
            raise GameNotInitializedError()

        self.current_state.controller.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(
        self,
        x: int,
        y: int,
        button: int,
        modifiers: int,
    ) -> None:
        """Handles releasing the mouse button."""
        if self.current_state is None:
            raise GameNotInitializedError()

        self.current_state.controller.on_mouse_release(
            x,
            y,
            button,
            modifiers,
        )

    def on_update(self, delta_time: float) -> None:
        """Handles updates."""
        if self.current_state is None:
            raise GameNotInitializedError()

        self.current_state.on_update(delta_time)
