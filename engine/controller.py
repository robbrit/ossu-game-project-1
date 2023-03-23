from typing import (
    Protocol,
)


class Controller(Protocol):
    """Protocol to define standard methods for controllers."""

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        ...

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        ...

    def on_mouse_motion(self, screen_x: int, screen_y: int, dx: int, dy: int) -> None:
        ...

    def on_update(self, delta_time: int) -> None:
        ...
