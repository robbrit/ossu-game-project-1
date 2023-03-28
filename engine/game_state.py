from typing import (
    Protocol,
)

import engine
from engine import (
    controller,
    view,
)


class GUI(Protocol):
    """A GUI is a set of buttons and images that the user interacts with."""

    @property
    def spec(self) -> "engine.gui.widgets.GUISpec":
        """A declarative form of the GUI, saying how it should be rendered."""
        ...


class GameAPI(Protocol):
    """A protocol for how game objects will interact with the engine."""

    def start_game(self) -> None:
        """Starts the game."""
        ...

    def change_region(self, name: str) -> None:
        """Switches the region of the game."""
        ...

    def show_gui(self, gui: GUI) -> None:
        """Shows a GUI."""
        ...


class GameState(Protocol):
    """Wraps a view and controller to represent a particular game state."""

    view: view.View
    controller: controller.Controller

    def setup(self, api: GameAPI) -> None:
        """Resets the game state."""
        ...

    def on_update(self, dt: int) -> None:
        """Updates the game state."""
        ...
