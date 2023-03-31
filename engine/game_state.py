from typing import (
    Protocol,
)

from engine import (
    controller,
    scripts,
    view,
)


class GameState(Protocol):
    """Wraps a view and controller to represent a particular game state."""

    view: view.View
    controller: controller.Controller

    def setup(self, api: scripts.GameAPI) -> None:
        """Resets the game state."""
        ...

    def on_update(self, dt: int) -> None:
        """Updates the game state."""
        ...
