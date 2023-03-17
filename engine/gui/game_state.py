from typing import (
    Optional,
    Tuple,
)


from engine import (
    game_state,
)

from engine.gui import (
    controller,
    view,
)


class GuiState:
    api: Optional[game_state.GameAPI]

    def __init__(self, viewport_size: Tuple[int, int]) -> None:
        self.controller = controller.GuiController()
        self.view = view.GuiView(viewport_size)

    def setup(self, api: game_state.GameAPI):
        self.view.setup()
        self.api = api
