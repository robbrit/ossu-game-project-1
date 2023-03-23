from typing import (
    Protocol,
    Tuple,
)


class View(Protocol):
    def setup(self) -> None:
        ...

    def on_draw(self) -> None:
        ...

    def on_update(self, delta_time: int) -> None:
        ...

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        ...
