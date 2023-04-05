from typing import (
    Optional,
)

import arcade.key

from engine import (
    scripts,
)
from engine.gui import widgets


class GuiController:
    """
    This class handles GUI-based interaction.
    """

    selected_button: Optional[widgets.Button]
    api: Optional[scripts.GameAPI]
    gui: scripts.GUI

    def __init__(self, initial_gui: scripts.GUI):
        self.selected_button = None
        self.api = None
        self.gui = initial_gui
        self.selected_button = self.gui.spec.initial_selected_button

    def setup(self, api: scripts.GameAPI) -> None:
        """Sets up the controller."""
        self.api = api

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handles key presses."""
        # pylint: disable=unused-argument

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handles key releases."""
        # py lint: disable=unused-argument

        if symbol == arcade.key.ENTER:
            self._activate_current_button()
        elif symbol == arcade.key.RIGHT:
            if self.selected_button.right is not None:
                # TODO(jon): current button should show unselected image.
                self._change_current_button(self.selected_button.right)
        elif symbol == arcade.key.LEFT:
            if self.selected_button.left is not None:
                self._change_current_button(self.selected_button.left)
        elif symbol == arcade.key.UP:
            if self.selected_button.up is not None:
                self._change_current_button(self.selected_button.up)
        elif symbol == arcade.key.DOWN:
            if self.selected_button.down is not None:
                self._change_current_button(self.selected_button.down)

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        """Handles mouse motion."""
        # pylint: disable=unused-argument

    def on_mouse_release(
        self,
        screen_x: int,
        screen_y: int,
        button: int,
        modifiers: int,
    ) -> None:
        """Handles mouse button release."""
        # pylint: disable=unused-argument

    def on_update(self, delta_time: float) -> None:
        """Handles updates."""
        # pylint: disable=unused-argument

    def _activate_current_button(self):
        if self.selected_button is None:
            return

        self.selected_button.action(self.api)

    def _change_current_button(self, button_name) -> None:
        for next_button in self.gui.spec.buttons:
            if button_name == next_button.name:
                self.selected_button = next_button
