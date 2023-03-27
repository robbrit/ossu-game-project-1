from typing import (
    Optional,
)

import arcade
import arcade.tilemap
from pyglet import math as pmath

from engine import (
    game_state,
    scripts,
)
from engine.ingame import game_sprite

TILE_SCALING = 1

PLAYER_MOVEMENT_SPEED = 5

# The distance in pixels from the center of the player object that we use for testing
# activions.
HITBOX_DISTANCE = 32

ACTIVATEABLE_OBJECTS = "Activateable Objects"


class Model:
    """
    This class represents the model layer. It manages maintenance of the state
    of the world.
    """

    api: game_state.GameAPI

    player_sprite: Optional[game_sprite.GameSprite]
    scene: Optional[arcade.Scene]
    physics_engine: Optional[arcade.PhysicsEngineSimple]

    # The tile map is created by the Tiled tool and loaded by our system. Most of the
    # game data will be stored there.
    # Things that the tile map must have:
    # * A tile layer called "Wall Tiles" containing all walls.
    #
    # They may have:
    # * An object layer called "Activateable Objects". All objects of this type must:
    #   * Have a custom property called "on_activate" that binds to a function that
    #     accepts a GameAPI object.
    #   * Be rectangular.
    #
    # The initial tile map must have:
    # * An object layer called "Key Points", containing an object named "Start".
    tile_map: Optional[arcade.tilemap.TileMap]
    activateable_objects: Optional[arcade.SpriteList]

    def __init__(self, api: game_state.GameAPI):
        self.api = api

        self.tile_map = arcade.load_tilemap(
            "assets/regions/Region1.json",
            TILE_SCALING,
            {
                "Wall Tiles": {
                    "use_spatial_hash": True,
                },
            },
        )

        self.activateable_objects = arcade.SpriteList(
            use_spatial_hash=True,
        )
        for obj in self.tile_map.object_lists.get(ACTIVATEABLE_OBJECTS, []):
            self.activateable_objects.append(self._create_object_sprite(obj))

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.scene.add_sprite_list(
            name=ACTIVATEABLE_OBJECTS,
            sprite_list=self.activateable_objects,
        )

        self._init_player()

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.tile_map.sprite_lists["Wall Tiles"],
        )

    def _init_player(self):
        start = [
            obj
            for obj in self.tile_map.object_lists["Key Points"]
            if obj.name == "Start"
        ]
        if not start:
            raise Exception("No start location defined.")

        self.player_sprite = game_sprite.GameSprite(
            "assets/sprites/player/spec.json",
        )

        self.player_sprite.center_x = start[0].shape[0]
        self.player_sprite.center_y = start[0].shape[1]
        self.scene.add_sprite("Player", self.player_sprite)

    def _create_object_sprite(self, obj: arcade.TiledObject) -> arcade.Sprite:
        # Find the bounding rectangle for all the points.
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        pixel_height = self.tile_map.height * self.tile_map.tile_height

        for x, y in obj.shape:
            # The y coordinates come in as negative values, and they're relative to the
            # top of the map. They need to be translated to values from the bottom.
            y = pixel_height + y
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)

        width = max_x - min_x
        height = max_y - min_y

        center_x = min_x + width / 2
        center_y = min_y + height / 2

        # Hit boxes in arcade need to be relative to the center.
        hit_box = [
            ((x - center_x), (pixel_height + y - center_y)) for x, y in obj.shape
        ]

        sprite = arcade.Sprite(
            center_x=center_x,
            center_y=center_y,
            hit_box_algorithm="Simple",
        )
        sprite.set_hit_box(hit_box)
        sprite.properties = obj.properties
        return sprite

    def on_update(self, delta_time: int) -> None:
        self.player_sprite.on_update(delta_time)
        self.physics_engine.update()

    def set_player_speed(
        self,
        vx: Optional[int] = None,
        vy: Optional[int] = None,
    ) -> None:
        """Sets the player's speed.

        Each direction may be set to None to avoid changing the speed in that
        direction.
        """
        if vx is not None:
            self.player_sprite.change_x = vx * PLAYER_MOVEMENT_SPEED

        if vy is not None:
            self.player_sprite.change_y = vy * PLAYER_MOVEMENT_SPEED

    def set_player_facing(self, facing_x: int, facing_y: int) -> None:
        """Sets the direction the player is facing."""
        self.player_sprite.facing_x = facing_x
        self.player_sprite.facing_y = facing_y

    def activate(self) -> None:
        """Activates whatever is in front of the player."""

        # Do a little bit of math to figure out where to place the hitbox.
        facing = pmath.Vec2(self.player_sprite.facing_x, self.player_sprite.facing_y)

        hitbox_center = facing.normalize().scale(HITBOX_DISTANCE)

        objects = arcade.get_sprites_at_point(
            (
                int(hitbox_center.x + self.player_sprite.center_x),
                int(hitbox_center.y + self.player_sprite.center_y),
            ),
            self.activateable_objects,
        )

        if not objects:
            return

        for obj in objects:
            callable = obj.properties.get("on_activate")

            if not callable:
                continue

            scripts.load_callable(callable)(self.api)
