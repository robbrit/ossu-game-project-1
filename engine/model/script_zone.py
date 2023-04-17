import arcade

from engine.model import shapes


class ScriptZone(arcade.Sprite):
    """A polygon in a map that can have a script tied to it."""

    def __init__(
        self,
        obj: arcade.TiledObject,
        world_pixel_height: int,
    ):
        shape = shapes.tiled_object_shape(obj)

        super().__init__(
            center_x=shape.center_x,
            # Tiled gives the Y coordinates as a negative from the top, but Arcade does
            # them starting from the bottom.
            center_y=world_pixel_height + shape.center_y,
            hit_box_algorithm="Simple",
        )

        # Hit boxes in arcade need to be relative to the center.
        hit_box = [
            ((x - shape.center_x), (y - shape.center_y)) for x, y in shape.points
        ]
        self.set_hit_box(hit_box)
        self.properties = {
            "name": obj.name,
        }

    @property
    def name(self) -> str:
        """Gets the name of this sprite."""
        return self.properties["name"]
