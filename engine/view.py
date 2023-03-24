from typing import (
    Protocol,
    Tuple,
)


class View(Protocol):
    """Defines an interface for how the engine talks to a view."""

    def setup(self) -> None:
        """Resets the game state."""
        ...

    def on_draw(self) -> None:
        """Renders the game."""
        ...

    def on_update(self, delta_time: int) -> None:
        """Called every game tick."""
        ...

    def to_world_coords(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Converts a set of screen coordinates into world coordinates.

        Screen coordinates are relative to the bottom left of the screen, but
        world coordinates are relative to the bottom left of the map. Some views
        will distinguish between these two if the camera is not showing the
        entire map.
        """
        ...
