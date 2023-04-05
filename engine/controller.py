from typing import (
    Protocol,
)


class Controller(Protocol):
    """Protocol to define standard methods for controllers."""

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handles when the user presses a key down."""

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handles when the user releases a key."""

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        """Handles when the user moves the mouse."""

    def on_mouse_release(
        self,
        screen_x: int,
        screen_y: int,
        button: int,
        modifiers: int,
    ) -> None:
        """Handles when the user releases a mouse button."""

    def on_update(self, delta_time: int) -> None:
        """Handles game tick updates."""
