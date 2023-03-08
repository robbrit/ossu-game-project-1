import arcade
import arcade.tilemap

from engine import (
    game_state,
    model,
)
from engine.ingame import game_state as ingame_state

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "OSSU Game Project"


class Core(arcade.Window):
    """
    Main application class.
    """

    game_state: game_state.GameState
    ingame_state: ingame_state.InGameState
    model: model.Model

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
        )

        self.model = model.Model()
        self.ingame_state = ingame_state.InGameState(
            self.model,
            (self.width, self.height),
        )
        self.state = None

    def setup(self) -> None:
        """Resets the game state."""
        self.model.setup()
        self.ingame_state.setup(self)

    def start_game(self) -> None:
        """Switches to the "in game" state."""
        self.game_state = self.ingame_state

    def show_gui(self, gui: game_state.GUI) -> None:
        raise NotImplementedError("gui state not implemented yet.")

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

    def on_update(self, delta_time: int) -> None:
        """Handles updates."""
        self.model.on_update(delta_time)
        self.game_state.controller.on_update(delta_time)
        self.game_state.view.on_update(delta_time)

    def run(self):
        """Runs the game."""
        self.setup()
        self.start_game()
        arcade.run()
