import numbers
from typing import (
    Any,
    Dict,
    NamedTuple,
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

KEY_POINTS = "Key Points"
SCRIPTED_OBJECTS = "Scripted Objects"


class RegionSpec(NamedTuple):
    """Specifies the details of a particular region."""

    tiled_mapfile: str
    wall_layer: str = "Wall Tiles"


class WorldSpec(NamedTuple):
    """Specifies the details for the entire world."""

    regions: Dict[str, RegionSpec]
    initial_region: str

    @classmethod
    def create(cls, data: Dict[str, Any]) -> "WorldSpec":
        return WorldSpec(
            regions={
                region_name: RegionSpec(**r)
                for region_name, r in data["regions"].items()
            },
            initial_region=data["initial_region"],
        )


class ScriptedObject(NamedTuple):
    """Ties a world object to a script."""

    sprite: arcade.Sprite
    owner: scripts.ScriptOwner
    script: scripts.Script


class Model:
    """
    This class represents the model layer. It manages maintenance of the state
    of the world.
    """

    api: game_state.GameAPI

    player_sprite: Optional[game_sprite.GameSprite]
    scene: Optional[arcade.Scene]
    physics_engine: Optional[arcade.PhysicsEngineSimple]

    time: int

    # The tile map is created by the Tiled tool and loaded by our system. Most of the
    # game data will be stored there.
    # Things that the tile map must have:
    # * A tile layer called "Wall Tiles" containing all walls.
    #
    # They may have:
    # * An object layer called "Scripted Objects". These objects can be scripted, which
    #   means the game can attach custom functionality to them. See engine/scripts.py
    #   for more details.
    #
    # The initial tile map must have:
    # * An object layer called "Key Points", containing an object named "Start".
    tilemaps: Dict[str, arcade.tilemap.TileMap]
    active_region: str
    scripted_objects: Dict[str, ScriptedObject]
    scripted_objects_spritelist: Optional[arcade.SpriteList]
    spec: str

    def __init__(self, api: game_state.GameAPI, spec: WorldSpec):
        self.api = api
        self.spec = spec
        self.time = 0

        self.player_sprite = game_sprite.GameSprite(
            "assets/sprites/player/spec.json",
        )

        self.tilemaps = {}

        for region_name, region in spec.regions.items():
            self.tilemaps[region_name] = arcade.load_tilemap(
                region.tiled_mapfile,
                TILE_SCALING,
                {
                    region.wall_layer: {
                        "use_spatial_hash": True,
                    },
                },
            )

        self.load_region(spec.initial_region, "Start")

    def load_region(self, region_name: str, start_location: str) -> None:
        """Loads a region by name."""
        self.active_region = region_name
        tilemap = self.tilemaps[region_name]
        region_spec = self.spec.regions[region_name]

        self.scripted_objects = {}
        self.scripted_objects_spritelist = arcade.SpriteList(
            use_spatial_hash=True,
        )
        for obj in tilemap.object_lists.get(SCRIPTED_OBJECTS, []):
            sprite = self._create_object_sprite(obj, tilemap)
            self.scripted_objects_spritelist.append(sprite)
            self.scripted_objects[obj.name] = ScriptedObject(
                sprite=sprite,
                owner=obj,
                script=self._load_object_script(obj),
            )

        self.scene = arcade.Scene.from_tilemap(tilemap)
        self.scene.add_sprite_list(
            name=SCRIPTED_OBJECTS,
            sprite_list=self.scripted_objects_spritelist,
        )
        self.scene.add_sprite("Player", self.player_sprite)

        self._reset_player(start_location, tilemap)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            tilemap.sprite_lists[region_spec.wall_layer],
        )

    def _reset_player(self, start_location: str, map: arcade.TileMap):
        start = [
            obj for obj in map.object_lists[KEY_POINTS] if obj.name == start_location
        ]
        if not start:
            raise Exception("No start location defined.")

        shape = start[0].shape

        if not isinstance(shape, list) or len(shape) != 2:
            raise Exception("Start location must be a point.")

        x, y = shape
        if not isinstance(x, numbers.Number) or not isinstance(y, numbers.Number):
            raise Exception("Start location must be a point.")

        self.player_sprite.center_x = start[0].shape[0]
        self.player_sprite.center_y = start[0].shape[1]

    def _create_object_sprite(
        self,
        obj: arcade.TiledObject,
        map: arcade.TileMap,
    ) -> arcade.Sprite:
        # Find the bounding rectangle for all the points.
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        pixel_height = map.height * map.tile_height

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
        sprite.properties = {
            "name": obj.name,
        }
        return sprite

    def _load_object_script(self, obj: arcade.TiledObject) -> scripts.Script:
        obj: scripts.Script
        if "script" in obj.properties:
            cls = scripts.load_script_class(obj.properties["script"])
            obj = cls()
        else:
            obj = scripts.ObjectScript(
                on_activate=obj.properties.get("on_activate"),
            )

        obj.set_api(self.api)
        return obj

    def on_update(self, delta_time: int) -> None:
        self.player_sprite.on_update(delta_time)
        self.physics_engine.update()
        self.time += delta_time

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
            self.scripted_objects_spritelist,
        )

        if not objects:
            return

        for obj in objects:
            name = obj.properties["name"]
            obj = self.scripted_objects[name]
            obj.script.on_activate(obj.owner, self.player_sprite)

    @property
    def width(self) -> int:
        """Gets the width of the map in number of tiles."""
        return self.tilemaps[self.active_region].width

    @property
    def height(self) -> int:
        """Gets the height of the map in number of tiles."""
        return self.tilemaps[self.active_region].height

    @property
    def tile_width(self) -> int:
        """Gets the tile width of the map in pixels."""
        return self.tilemaps[self.active_region].tile_width

    @property
    def tile_height(self) -> int:
        """Gets the tile height of the map in pixels."""
        return self.tilemaps[self.active_region].tile_height

    @property
    def game_time(self) -> int:
        '''Gets the in-game time in seconds.'''
        return int(self.time)
