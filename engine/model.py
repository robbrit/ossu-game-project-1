import numbers
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
    Tuple,
)

import arcade
import arcade.tilemap
from pyglet import math as pmath

from engine import (
    scripts,
    spec,
)
from engine.ingame import game_sprite

TILE_SCALING = 1

PLAYER_MOVEMENT_SPEED = 5

# The distance in pixels from the center of the player object that we use for testing
# activions.
HITBOX_DISTANCE = 32
HITBOX_WIDTH = 64
HITBOX_HEIGHT = 32

KEY_POINTS = "Key Points"
SCRIPTED_OBJECTS = "Scripted Objects"
NPCS = "NPCs"


class ScriptedObject(NamedTuple):
    """Ties a world object to a script."""

    sprite: arcade.Sprite
    owner: scripts.ScriptOwner
    script: scripts.Script


def _pull_script_args(prefix: str, properties: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts a set of arguments from a dict that has a certain prefix.

    The prefix is stripped from the keys in the result.
    """
    return {
        key.removeprefix(prefix): value
        for key, value in properties.items()
        if key.startswith(prefix)
    }


class Model:
    """
    This class represents the model layer. It manages maintenance of the state
    of the world.
    """

    api: scripts.GameAPI

    player_sprite: game_sprite.GameSprite
    scene: Optional[arcade.Scene]
    physics_engine: Optional[arcade.PhysicsEngineSimple]

    sec_passed: float

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

    _spec: spec.GameSpec

    def __init__(
        self,
        api: scripts.GameAPI,
        game_spec: spec.GameSpec,
    ):
        self.api = api
        self._spec = game_spec
        self.sec_passed = 0.0

        self.player_sprite = game_sprite.GameSprite(game_spec.player_spec)

        self.tilemaps = {}

        for region_name, region in game_spec.world.regions.items():
            self.tilemaps[region_name] = arcade.load_tilemap(
                region.tiled_mapfile,
                TILE_SCALING,
                {
                    region.wall_layer: {
                        "use_spatial_hash": True,
                    },
                },
            )

        self.load_region(game_spec.world.initial_region, "Start")

    def load_region(self, region_name: str, start_location: str) -> None:
        """Loads a region by name."""
        self.active_region = region_name
        tilemap = self.tilemaps[region_name]
        region_spec = self._spec.world.regions[region_name]

        self.scene = arcade.Scene.from_tilemap(tilemap)
        self._load_scripted_objects(tilemap)

        self.scene.add_sprite("Player", self.player_sprite)

        self._reset_player(start_location, tilemap)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            tilemap.sprite_lists[region_spec.wall_layer],
        )

    def _load_scripted_objects(self, tilemap: arcade.TileMap) -> None:
        self.scripted_objects = {}
        self.scene.add_sprite_list(SCRIPTED_OBJECTS, use_spatial_hash=True)

        sprites = []

        for obj in tilemap.object_lists.get(SCRIPTED_OBJECTS, []):
            sprite = self._create_object_sprite(obj, tilemap)
            sprites.append(sprite)
            self.scripted_objects[obj.name] = ScriptedObject(
                sprite=sprite,
                owner=obj,
                script=self._load_object_script(obj),
            )

        for obj in tilemap.object_lists.get(NPCS, []):
            sprite_spec = self._spec.sprites[obj.properties["spec"]]
            script = None
            if "script" in obj.properties:
                script_cls = scripts.load_script_class(obj.properties["script"])
                script = script_cls()
                script.set_api(self.api)

            sprite = self.create_sprite(sprite_spec, obj.name, obj.shape, script)

        self.scene.get_sprite_list(SCRIPTED_OBJECTS).extend(sprites)

    def create_sprite(
        self,
        sprite_spec: spec.GameSpriteSpec,
        name: str,
        start_location: Tuple[int, int],
        script: Optional[scripts.Script],
    ) -> arcade.Sprite:
        """Adds a sprite to the model."""
        sprite = game_sprite.GameSprite(sprite_spec)
        sprite.properties = {
            "name": name,
        }
        sprite.center_x = start_location[0]
        sprite.center_y = start_location[1]

        if script:
            self.scene.get_sprite_list(SCRIPTED_OBJECTS).append(sprite)
            self.scripted_objects[name] = ScriptedObject(
                sprite=sprite,
                owner=sprite,
                script=script,
            )
        else:
            # TODO(rob): Handle non-scripted sprites.
            raise NotImplementedError("Non-scripted sprites are not supported yet.")

        return sprite

    def _reset_player(self, start_location: str, tilemap: arcade.TileMap):
        start = [
            obj
            for obj in tilemap.object_lists[KEY_POINTS]
            if obj.name == start_location
        ]
        if not start:
            raise ValueError("No start location defined.")

        shape = start[0].shape

        if not isinstance(shape, list) or len(shape) != 2:
            raise TypeError("Start location must be a point.")

        x, y = shape
        if not isinstance(x, numbers.Number) or not isinstance(y, numbers.Number):
            raise TypeError("Start location must be a point.")

        self.player_sprite.center_x = start[0].shape[0]
        self.player_sprite.center_y = start[0].shape[1]

    def _create_object_sprite(
        self,
        obj: arcade.TiledObject,
        tilemap: arcade.TileMap,
    ) -> arcade.Sprite:
        # Find the bounding rectangle for all the points.
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        pixel_height = tilemap.height * tilemap.tile_height

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
                on_activate_args=_pull_script_args("on_activate_", obj.properties),
                on_collide=obj.properties.get("on_collide"),
                on_collide_args=_pull_script_args("on_collide_", obj.properties),
            )

        obj.set_api(self.api)
        return obj

    def on_update(self, delta_time: float) -> None:
        """Updates the model."""
        self.player_sprite.on_update(delta_time)
        self._prevent_oob()
        self.physics_engine.update()
        self._handle_collisions()
        self.sec_passed += delta_time

    def _handle_collisions(self) -> None:
        """Handles any collisions between different objects."""
        collisions = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene.get_sprite_list(SCRIPTED_OBJECTS),
            ],
        )

        for collision in collisions:
            obj = self.scripted_objects[collision.properties["name"]]
            obj.script.on_collide(obj.owner, self.player_sprite)

    def _prevent_oob(self) -> None:
        """Prevents the player from going out-of-bounds."""
        map_width = self.width * self.tile_width
        map_height = self.height * self.tile_height

        vx = self.player_sprite.change_x
        vy = self.player_sprite.change_y

        new_x = self.player_sprite.center_x + vx
        new_y = self.player_sprite.center_y + vy
        new_vx = None
        new_vy = None

        if (new_x <= 0 and vx < 0) or (new_x >= map_width and vx > 0):
            new_vx = 0

        if (new_y <= 0 and vy < 0) or (new_y >= map_height and vy > 0):
            new_vy = 0

        self.set_player_speed(new_vx, new_vy)

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

        hitbox_corners = [
            (-HITBOX_WIDTH / 2, -HITBOX_HEIGHT / 2),
            (HITBOX_WIDTH / 2, -HITBOX_HEIGHT / 2),
            (HITBOX_WIDTH / 2, HITBOX_HEIGHT / 2),
            (-HITBOX_WIDTH / 2, HITBOX_HEIGHT / 2),
        ]
        hitbox_sprite = arcade.Sprite(
            center_x=hitbox_center.x + self.player_sprite.center_x,
            center_y=hitbox_center.y + self.player_sprite.center_y,
        )
        hitbox_sprite.set_hit_box(
            [
                (corner_x + hitbox_center.x, corner_y + hitbox_center.y)
                for corner_x, corner_y in hitbox_corners
            ]
        )
        objects = arcade.check_for_collision_with_list(
            hitbox_sprite, self.scene.get_sprite_list(SCRIPTED_OBJECTS)
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
    def game_time_sec(self) -> float:
        """Gets the in-game time in seconds."""
        return self.sec_passed
