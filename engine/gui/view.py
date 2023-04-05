from typing import (
    Optional,
    Tuple,
)

from arcade import gui

from engine import scripts


class GuiView:
    """
    Manages rendering GUIs.
    """

    api: Optional[scripts.GameAPI]
    gui: scripts.GUI

    def __init__(self, initial_gui: scripts.GUI):
        self.api = None
        self.gui = initial_gui
        self.manager = gui.UIManager()
        self.manager.enable()

    def setup(self, api: scripts.GameAPI) -> None:
        """Sets up the view."""
        self.api = api

    def on_draw(self) -> None:
        """ "Renders the view."""
        self.gui.draw()
        self.manager.draw()

    def on_update(self, delta_time: float) -> None:
        """Updates the view."""
        # pylint: disable=unused-argument

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Converts a set of screen coordinates into world coordinates.

        For a GUI view, there is no difference, so this function is a no-op.
        """
        return screen_x, screen_y

    def set_gui(self, _gui: scripts.GUI) -> None:
        """Sets the GUI for the view."""
        self.manager.clear()
        self.gui = _gui
        self.gui.set_api(self.api)
        self.gui.set_manager(self.manager)
