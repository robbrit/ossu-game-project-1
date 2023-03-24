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
    """Defines the GUI state."""

    api: Optional[game_state.GameAPI]

    def __init__(
        self,
        initial_gui: game_state.GUI,
    ) -> None:
        self.controller = controller.GuiController(initial_gui)
        self.view = view.GuiView(initial_gui)

    def setup(self, api: game_state.GameAPI):
        self.view.setup()
        self.controller.setup(api)
        self.api = api

    def set_gui(self, gui: game_state.GUI) -> None:
        self.view.set_gui(gui)
