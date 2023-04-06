from typing import (
    Protocol,
)

from engine import (
    controller,
    view,
)


class GameState(Protocol):
    """Wraps a view and controller to represent a particular game state."""

    def setup(self) -> None:
        """Resets the game state."""

    def on_update(self, delta_time: float) -> None:
        """Updates the game state."""

    @property
    def controller(self) -> controller.Controller:
        """Gets the controller for this state."""

    @property
    def view(self) -> view.View:
        """Gets the view for this state."""
