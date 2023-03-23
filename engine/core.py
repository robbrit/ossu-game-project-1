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
    Main application class.
    """

    initial_gui: game_state.GUI
    game_state: game_state.GameState
    ingame_state: ingame_state.InGameState
    model: model.Model

    def __init__(self, initial_gui: game_state.GUI):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
        )

        self.model = model.Model()
        # TODO(rob): Probably should pull the game logic out of the engine and
        # into the game code.
        viewport = (self.width, self.height)
        self.initial_gui = initial_gui
        self.gui_state = gui_game_state.GuiState(initial_gui)
        self.ingame_state = ingame_state.InGameState(self.model, viewport)
        self.state = None

    def setup(self) -> None:
        """Resets the game state."""
        self.model.setup()
        self.gui_state.setup(self)
        self.ingame_state.setup(self)

    def start_game(self) -> None:
        """Switches to the "in game" state."""
        self.game_state = self.ingame_state

    def show_gui(self, gui: game_state.GUI) -> None:
        self.gui_state.set_gui(gui)
        self.game_state = self.gui_state

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

    def on_update(self, delta_time: int) -> None:
        """Handles updates."""
        self.model.on_update(delta_time)
        self.game_state.controller.on_update(delta_time)
        self.game_state.view.on_update(delta_time)

    def run(self):
        """Runs the game."""
        self.setup()
        self.show_gui(self.initial_gui)
        arcade.run()
