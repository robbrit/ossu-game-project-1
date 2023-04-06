from engine import (
    scripts,
)


class GuiController:
    """
    This class handles GUI-based interaction.
    """

    api: scripts.GameAPI
    gui: scripts.GUI

    def __init__(self, api: scripts.GameAPI, initial_gui: scripts.GUI):
        self.api = api
        self.gui = initial_gui

    def setup(self) -> None:
        """Sets up the controller."""

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handles key presses."""
        # pylint: disable=unused-argument

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handles key releases."""
        # pylint: disable=unused-argument

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
