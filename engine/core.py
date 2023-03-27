import arcade
import arcade.tilemap

from engine import (
    game_state,
    model,
)
from engine.gui import game_state as gui_game_state
from engine.ingame import game_state as ingame_state

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "OSSU Game Project"


class Core(arcade.Window):
    """
    Main application class, wraps everything.

    The game uses an MVC pattern:
    * Models - capture the state of the world in the game: players, regions, enemies,
      etc.
    * Views - handle rendering anything.
    * Controllers - handles interacting with the user.

    There's only one model, but the views and controllers are wrapped by GameState
    objects. The game can be in one of two possible states:
    * In a GUI - the model does not update, we render some sort of GUI, and all controls
      go to manipulating the GUI.
    * In the game - the model updates and all controls go to managing the character.
    """

    game_state: game_state.GameState
    gui_state: gui_game_state.GuiState
    ingame_state: ingame_state.InGameState

    model: model.Model
    initial_gui: game_state.GUI

    def __init__(self, initial_gui: game_state.GUI):
        """Constructor.

        Args:
            initial_gui: The GUI screen to show when the game starts.
        """
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
        )

        self.model = model.Model(self)
        self.initial_gui = initial_gui
        self.gui_state = gui_game_state.GuiState(initial_gui)
        self.ingame_state = ingame_state.InGameState(
            self.model,
            (self.width, self.height),
        )
        self.game_state = None

    def setup(self) -> None:
        """Resets the game state."""
        self.model.setup()
        self.gui_state.setup(self)
        self.ingame_state.setup(self)

    def start_game(self) -> None:
        """Switches to the "in game" state."""
        self.game_state = self.ingame_state

    def show_gui(self, gui: game_state.GUI) -> None:
        """Switches to the "GUI" state, and displays a certain GUI."""
        self.gui_state.set_gui(gui)
        self.game_state = self.gui_state

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
        self.clear()
        self.game_state.view.on_draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handles incoming key presses."""
        self.game_state.controller.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handles incoming key releases."""
        self.game_state.controller.on_key_release(symbol, modifiers)

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        self.game_state.controller.on_mouse_motion(screen_x, screen_y, dx, dy)

    def on_mouse_release(
        self,
        screen_x: int,
        screen_y: int,
        button: int,
        modifiers: int,
    ) -> None:
        self.game_state.controller.on_mouse_release(
            screen_x,
            screen_y,
            button,
            modifiers,
        )

    def on_update(self, delta_time: int) -> None:
        """Handles updates."""
        self.model.on_update(delta_time)
        self.game_state.controller.on_update(delta_time)
        self.game_state.view.on_update(delta_time)
