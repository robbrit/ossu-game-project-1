from typing import (
    Optional,
    Tuple,
)


from engine import (
    game_state,
    model,
)

from engine.ingame import (
    controller,
    view,
)


class InGameState:
    """Wraps the "in game" state."""

    api: Optional[game_state.GameAPI]
    model: model.Model

    def __init__(self, model: model.Model, viewport_size: Tuple[int, int]) -> None:
        self.model = model
        self.view = view.InGameView(model, viewport_size)
        self.controller = controller.InGameController(model, self.view)

    def setup(self, api: game_state.GameAPI):
        self.view.setup()
        self.api = api

    def on_update(self, dt: int) -> None:
        self.model.on_update(dt)
        self.view.on_update(dt)
        self.controller.on_update(dt)
