from typing import (
    Optional,
    Tuple,
)


from engine import (
    model,
    scripts,
)

from engine.ingame import (
    controller,
    view,
)


class InGameState:
    """Wraps the "in game" state."""

    api: Optional[scripts.GameAPI]
    game_model: model.Model

    def __init__(self, game_model: model.Model, viewport_size: Tuple[int, int]) -> None:
        self.game_model = game_model
        self.view = view.InGameView(game_model, viewport_size)
        self.controller = controller.InGameController(game_model, self.view)

    def setup(self, api: scripts.GameAPI):
        """Sets up the in-game state."""
        self.view.setup()
        self.api = api

    def on_update(self, delta_time: float) -> None:
        """Triggers an update for the game."""
        self.game_model.on_update(delta_time)
        self.view.on_update(delta_time)
        self.controller.on_update(delta_time)
