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
    api: Optional[game_state.GameAPI]

    def __init__(self, model: model.Model, viewport_size: Tuple[int, int]) -> None:
        self.view = view.InGameView(model, viewport_size)
        self.controller = controller.InGameController(model, self.view)

    def setup(self, api: game_state.GameAPI):
        self.view.setup()
        self.api = api
