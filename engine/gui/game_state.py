from engine import (
    controller,
    scripts,
    view,
)
from engine.gui import (
    controller as gui_controller,
    view as gui_view,
)


class GuiState:
    """Defines the GUI state."""

    api: scripts.GameAPI
    _controller: gui_controller.GuiController
    _view: gui_view.GuiView

    def __init__(
        self,
        api: scripts.GameAPI,
        initial_gui: scripts.GUI,
    ) -> None:
        self.api = api
        self._controller = gui_controller.GuiController(api, initial_gui)
        self._view = gui_view.GuiView(api, initial_gui)

    def setup(self):
        """Sets up the GUI state."""
        self._view.setup()
        self._controller.setup()

    def set_gui(self, gui: scripts.GUI) -> None:
        """Sets the GUI for the game state."""
        self._view.set_gui(gui)

    def on_update(self, delta_time: float) -> None:
        """Triggers an update for the gui."""
        self._view.on_update(delta_time)
        self._controller.on_update(delta_time)

    @property
    def controller(self) -> controller.Controller:
        """Gets the controller for this state."""
        return self._controller

    @property
    def view(self) -> view.View:
        """Gets the view for this state."""
        return self._view
