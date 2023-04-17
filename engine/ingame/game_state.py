from typing import (
    Optional,
    Tuple,
)


from engine import (
    controller,
    model,
    scripts,
    view,
)

from engine.ingame import (
    controller as game_controller,
    view as game_view,
)


class InGameState:
    """Wraps the "in game" state."""

    game_model: model.Model
    controller: controller.Controller
    view: view.View

    def __init__(
        self,
        game_model: model.Model,
        viewport_size: Tuple[int, int],
        ingame_gui: Optional[scripts.GUI],
    ) -> None:
        self.game_model = game_model
        self.view = game_view.InGameView(game_model, viewport_size, gui=ingame_gui)
        self.controller = game_controller.InGameController(game_model, self.view)

    def setup(self) -> None:
        """Sets up the in-game state."""
        self.view.setup()

    def on_update(self, delta_time: float) -> None:
        """Triggers an update for the game."""
        self.game_model.on_update(delta_time)
        self.view.on_update(delta_time)
        self.controller.on_update(delta_time)
