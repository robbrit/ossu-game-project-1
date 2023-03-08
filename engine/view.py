from typing import (
    Protocol,
)


class View(Protocol):
    def setup(self) -> None:
        ...

    def on_draw(self) -> None:
        ...

    def on_update(self, delta_time: int) -> None:
        ...
