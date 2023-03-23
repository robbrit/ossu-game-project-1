from typing import (
    Optional,
)

import arcade
import arcade.tilemap

from engine.ingame import game_sprite

TILE_SCALING = 1

PLAYER_MOVEMENT_SPEED = 5


class Model:
    """
    This class represents the model layer. It manages maintenance of the state
    of the world.
    """

    player_sprite: Optional[game_sprite.GameSprite]
    scene: Optional[arcade.Scene]
    tile_map: Optional[arcade.tilemap.TileMap]
    physics: Optional[arcade.PhysicsEngineSimple]

    def __init__(self):
        self.player_sprite = None
        self.scene = None
        self.tile_map = None
        self.physics = None

    def setup(self):
        self.tile_map = arcade.load_tilemap(
            "assets/regions/Region1.json",
            TILE_SCALING,
            {
                "Wall Tiles": {
                    "use_spatial_hash": True,
                },
            },
        )
        start = [
            obj
            for obj in self.tile_map.object_lists["Key Points"]
            if obj.name == "Start"
        ]
        if not start:
            raise Exception("No start location defined.")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite_list("Player")

        self.player_sprite = game_sprite.GameSprite(
            "assets/sprites/player/spec.json",
        )

        self.player_sprite.center_x = start[0].shape[0]
        self.player_sprite.center_y = start[0].shape[1]
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            self.tile_map.sprite_lists["Wall Tiles"],
        )

    def on_update(self, delta_time: int) -> None:
        self.player_sprite.on_update(delta_time)
        self.physics_engine.update()

    def set_player_speed(
        self,
        vx: Optional[int] = None,
        vy: Optional[int] = None,
    ) -> None:
        if vx is not None:
            self.player_sprite.change_x = vx * PLAYER_MOVEMENT_SPEED

        if vy is not None:
            self.player_sprite.change_y = vy * PLAYER_MOVEMENT_SPEED

    def set_player_facing(self, facing_x: int, facing_y: int) -> None:
        self.player_sprite.facing_x = facing_x
        self.player_sprite.facing_y = facing_y
