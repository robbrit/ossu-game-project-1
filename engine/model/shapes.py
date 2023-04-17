import dataclasses
import numbers
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


@dataclasses.dataclass
class Point:
    """Represents a single 2D point."""

    x: float
    y: float

    @property
    def center_x(self) -> float:
        """Gets the X coordinate of the center point."""
        return self.x

    @property
    def center_y(self) -> float:
        """Gets the Y coordinate of the center point."""
        return self.y

    @property
    def points(self) -> Sequence[Tuple[float, float]]:
        """Gets the sequence of points making up this shape."""
        return [(self.x, self.y)]


def tiled_object_shape(obj: arcade.TiledObject) -> Shape:
    """Gets the shape for the given Tiled object."""

    shape_iter = iter(obj.shape)
    item = next(shape_iter)

    if isinstance(item, numbers.Number):
        # The shape is a sequence of numbers, which gives us a point.
        if len(obj.shape) != 2:
            raise ValueError("Only 2D points are supported.")

        return Point(obj.shape[0], obj.shape[1])

    # Now blindly assume it's a polygon.
    shape: Sequence[Tuple[float, float]]
    shape = obj.shape  # type: ignore

    return Polygon(shape)
