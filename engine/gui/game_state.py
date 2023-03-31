from typing import (
    Optional,
    Tuple,
)


from engine import (
    scripts,
)

from engine.gui import (
    controller,
    view,
)


class GuiState:
    """Defines the GUI state."""

    api: Optional[scripts.GameAPI]

    def __init__(
        self,
        initial_gui: scripts.GUI,
    ) -> None:
        self.controller = controller.GuiController(initial_gui)
        self.view = view.GuiView(initial_gui)

    def setup(self, api: scripts.GameAPI):
        self.view.setup()
        self.controller.setup(api)
        self.api = api

    def set_gui(self, gui: scripts.GUI) -> None:
        self.view.set_gui(gui)

    def on_update(self, dt: int) -> None:
        self.view.on_update(dt)
        self.controller.on_update(dt)
