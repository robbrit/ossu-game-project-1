from typing import (
    Protocol,
)


class Controller(Protocol):
    """Protocol to define standard methods for controllers."""

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        ...

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        ...

    def on_update(self, delta_time: int) -> None:
        ...
