from typing import (
    Protocol,
    Sequence,
    Tuple,
)

import arcade


class Shape(Protocol):
    """Represents a shape of some kind."""

    @property
    def center_x(self) -> float:
        """Gets the X coordinate of the center point."""

    @property
    def center_y(self) -> float:
        """Gets the Y coordinate of the center point."""

    @property
    def points(self) -> Sequence[Tuple[float, float]]:
        """Gets the sequence of points making up this shape."""


class Polygon:
    """Represents a polygon."""

    center_x: float
    center_y: float
    points: Sequence[Tuple[float, float]]

    def __init__(self, points: Sequence[Tuple[float, float]]):
        if not points:
            raise ValueError("Polygon must have at least one point.")

        self.points = points

        total_x = 0.0
        total_y = 0.0

        for x, y in points:
            total_x += x
            total_y += y

        self.center_x = total_x / len(points)
        self.center_y = total_y / len(points)


def tiled_object_shape(obj: arcade.TiledObject) -> Shape:
    """Gets the shape for the given Tiled object."""

    # TODO(rob): Support points/lines.
    shape: Sequence[Tuple[float, float]]
    shape = obj.shape  # type: ignore

    return Polygon(shape)
