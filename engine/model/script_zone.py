from typing import (
    Tuple,
)

import arcade

from engine import scripts
from engine.model import (
    game_sprite,
    shapes,
)


class ScriptZone(game_sprite.GameSprite):
    """A polygon in a map that can have a script tied to it."""

    _shape: shapes.Shape

    def __init__(
        self,
        obj: arcade.TiledObject,
        world_pixel_height: int,
        script: scripts.Script,
    ):
        super().__init__(name=obj.name or "", script=script)

        shape = shapes.tiled_object_shape(obj)
        self._shape = shape

        # Hit boxes in arcade need to be relative to the center.
        hit_box = [
            ((x - shape.center_x), (y - shape.center_y)) for x, y in shape.points
        ]
        self.center_x = shape.center_x
        # Tiled gives the Y coordinates as a negative from the top, but Arcade does
        # them starting from the bottom.
        self.center_y = world_pixel_height + shape.center_y
        self.hit_box_algorithm = "Simple"
        self.set_hit_box(hit_box)
        self.properties = {
            "solid": (obj.properties or {}).get("solid", False),
        }

    @property
    def location(self) -> Tuple[float, float]:
        """Gets the location of this script zone."""
        return (self._shape.center_x, self._shape.center_y)

    @property
    def speed(self) -> Tuple[float, float]:
        """Gets the speed of the script owner."""
        return (0.0, 0.0)

    @speed.setter
    def speed(self, value: Tuple[float, float]) -> None:
        """Sets the speed of the script owner."""
        # Deliberately does nothing. Zones don't move.

    @property
    def facing(self) -> Tuple[float, float]:
        """Gets the facing direction of the script owner."""
        return (0.0, 0.0)

    @facing.setter
    def facing(self, value: Tuple[float, float]) -> None:
        """Sets the facing direction of the script owner."""
        # Deliberately does nothing. Zones don't face anywhere.
