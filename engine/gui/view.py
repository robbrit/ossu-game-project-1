from typing import (
    Tuple,
)

from engine import scripts


class GuiView:
    """
    Manages rendering GUIs.
    """

    gui: scripts.GUI

    def __init__(self, initial_gui: scripts.GUI):
        self.gui = initial_gui

    def setup(self) -> None:
        # TODO(rob): Handle any setup.
        pass

    def on_draw(self) -> None:
        self.gui.draw()

    def on_update(self, delta_time: int) -> None:
        pass

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        return screen_x, screen_y

    def set_gui(self, gui: scripts.GUI) -> None:
        self.gui = gui
