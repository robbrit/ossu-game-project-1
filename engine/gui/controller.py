from typing import (
    Optional,
)

import arcade.key

from engine import game_state
from engine.gui import widgets


class GuiController:
    """
    This class handles GUI-based interaction.
    """

    selected_button: Optional[widgets.Button]
    api: Optional[game_state.GameAPI]
    gui: game_state.GUI

    def __init__(self, initial_gui: game_state.GUI):
        self.selected_button = None
        self.api = None
        self.gui = initial_gui
        self.selected_button = self.gui.spec.initial_selected_button

    def setup(self, api: game_state.GameAPI) -> None:
        self.api = api

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # Don't really need to do anything here.
        pass

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ENTER:
            self._activate_current_button()

        # TODO(rob): Handle activate, cancel, and direction keys.

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        pass

    def on_mouse_release(
        self,
        screen_x: int,
        screen_y: int,
        button: int,
        modifiers: int,
    ) -> None:
        pass

    def on_update(self, delta_time: int) -> None:
        pass

    def _activate_current_button(self):
        if self.selected_button is None:
            return

        self.selected_button.action(self.api)
