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
        self.api = api

    def on_draw(self) -> None:
        self.gui.draw()
        self.manager.draw()

    def on_update(self, delta_time: int) -> None:
        pass

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        return screen_x, screen_y

    def set_gui(self, gui: scripts.GUI) -> None:
        self.manager.clear()
        self.gui = gui
        self.gui.set_api(self.api)
        self.gui.set_manager(self.manager)
