from typing import (
    Optional,
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
        """Sets up the GUI state."""
        self.view.setup(api)
        self.controller.setup(api)
        self.api = api

    def set_gui(self, gui: scripts.GUI) -> None:
        """Sets the GUI for the game state."""
        self.view.set_gui(gui)

    def on_update(self, delta_time: float) -> None:
        """Triggers an update for the gui."""
        self.view.on_update(delta_time)
        self.controller.on_update(delta_time)
