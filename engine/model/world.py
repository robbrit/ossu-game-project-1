import dataclasses
import numbers
from typing import (
    Any,
    cast,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
)

import arcade
import arcade.tilemap
from pyglet import math as pmath

from engine import (
    scripts,
    spec,
)
from engine.model import (
    game_sprite,
    physics,
    script_zone,
    shapes,
)

TILE_SCALING = 1

PLAYER_MOVEMENT_SPEED = 250

# The distance in pixels from the center of the player object that we use for testing
# activions.
HITBOX_DISTANCE = 32

KEY_POINTS = "Key Points"
SCRIPTED_OBJECTS = "Scripted Objects"
NPCS = "NPCs"


class SceneNotInitialized(Exception):
    """Raised when methods are called on the model before the scene was initialized."""


class NoScript(Exception):
    """Raised when we attempt to load a script on an object that doesn't have one."""


@dataclasses.dataclass
class RegionState:
    """Stores the state of a region."""

    # Mapping from scripted object names to their state.
    object_states: Dict[str, Dict[str, Any]] = dataclasses.field(default_factory=dict)


class World:
    """
    This class represents the world. It manages maintenance of the state of the world.
    """

    # TODO(rob): This class is getting big and incohesive. Some refactors that would
    # clean it up:
    # - Make RegionState a bit smarter, have it manage serialization of itself.
    # - Create a PlayerSprite object that wraps all the player-specific stuff.
    # - Make as much as possible private; things outside this class are starting to poke
    #   into it which adds extra coupling.

    api: scripts.GameAPI

    player_sprite: game_sprite.GameSprite
    player_state: Dict[str, Any]

    scene: Optional[arcade.Scene]
    physics_engine: Optional[physics.Engine]

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
    region_states: Dict[str, RegionState]
    regions_loaded: Set[str]

    _game_sprites: Dict[str, game_sprite.GameSprite]

    _spec: spec.GameSpec

    in_update: bool
    sprites_to_add: Dict[str, game_sprite.GameSprite]

    def __init__(
        self,
        api: scripts.GameAPI,
        game_spec: spec.GameSpec,
        initial_player_state: Dict[str, Any],
    ):
        self.api = api
        self._spec = game_spec
        self.sec_passed = 0.0

        self.player_sprite = game_sprite.GameSprite(
            name="player",
            sprite_spec=game_spec.player_spec,
        )
        self.player_state = initial_player_state

        self.tilemaps = {}
        self.region_states = {}
        self._game_sprites = {}
        self.active_region = ""
        self.regions_loaded = set()

        self.in_update = False
        self.sprites_to_add = {}

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
        if self.active_region != "":
            self.region_states[self.active_region] = RegionState(
                object_states={
                    sprite.name: sprite.script.state
                    for sprite in self._game_sprites.values()
                    if sprite.script is not None
                },
            )

        self.active_region = region_name
        tilemap = self.tilemaps[region_name]
        region_spec = self._spec.world.regions[region_name]

        if region_name not in self.region_states:
            region_state = RegionState()
        else:
            region_state = self.region_states[region_name]

        is_first_load = region_name not in self.regions_loaded
        self.regions_loaded.add(region_name)

        self.scene = arcade.Scene.from_tilemap(tilemap)
        self._load_scripted_objects(tilemap, region_state, is_first_load)

        self.scene.add_sprite("Player", self.player_sprite)

        self._reset_player(start_location, tilemap)

        physics_objs: List[game_sprite.GameSprite] = [self.player_sprite]
        physics_objs.extend(self._game_sprites.values())

        self.physics_engine = physics.Engine(
            physics_objs,
            tilemap.sprite_lists[region_spec.wall_layer],
            map_size=(
                self.width * self.tile_width,
                self.height * self.tile_height,
            ),
        )

    def _load_scripted_objects(
        self,
        tilemap: arcade.TileMap,
        region_state: RegionState,
        is_first_load: bool,
    ) -> None:
        if self.scene is None:
            raise SceneNotInitialized()

        self._game_sprites = {}
        self.scene.add_sprite_list(SCRIPTED_OBJECTS, use_spatial_hash=True)

        sprites = []
        script: Optional[scripts.Script] = None
        sprite: game_sprite.GameSprite

        world_pixel_height = tilemap.tile_height * tilemap.height

        for obj in tilemap.object_lists.get(SCRIPTED_OBJECTS, []):
            if obj.properties is None:
                raise ValueError("Missing properties attribute for scripted object.")

            if obj.name is None:
                raise ValueError("Missing name attribute for scripted object.")

            script = self._script_from_tiled_object(obj)
            script.state = region_state.object_states.get(obj.name, {})

            sprite = script_zone.ScriptZone(
                obj,
                world_pixel_height,
                script,
            )
            sprites.append(sprite)

            if is_first_load:
                script.on_start(sprite)

            self._game_sprites[obj.name] = sprite

        for obj in tilemap.object_lists.get(NPCS, []):
            if obj.properties is None:
                raise ValueError("NPC must have properties set.")

            if obj.name is None:
                raise ValueError("NPC must have name set.")

            sprite_spec = self._spec.sprites[obj.properties["spec"]]
            try:
                script = self._load_script(obj.properties)
                script.state = region_state.object_states.get(obj.name, {})
            except NoScript:
                script = None

            shape: Tuple[float, float]
            # Do some hackery to get the type checker to be happy.
            # TODO(rob): We should probably ensure that the shape is a point and not
            # a rectangle or something.
            shape = obj.shape  # type: ignore

            sprite = self._create_sprite(
                sprite_spec,
                obj.name,
                shape,
                script,
                is_first_load=is_first_load,
            )
            sprite.properties["solid"] = obj.properties.get("solid", False)

        self.scene.get_sprite_list(SCRIPTED_OBJECTS).extend(sprites)

    def create_sprite(
        self,
        sprite_spec: spec.GameSpriteSpec,
        name: str,
        start_location: Tuple[float, float],
        script: Optional[scripts.Script],
    ) -> arcade.Sprite:
        """Adds a sprite to the model."""
        return self._create_sprite(
            sprite_spec,
            name,
            start_location,
            script,
            is_first_load=True,
        )

    def _create_sprite(
        self,
        sprite_spec: spec.GameSpriteSpec,
        name: str,
        start_location: Tuple[float, float],
        script: Optional[scripts.Script],
        is_first_load: bool,
    ) -> game_sprite.GameSprite:
        if self.scene is None:
            raise SceneNotInitialized()

        if not script:
            raise NotImplementedError("Non-scripted sprites are not supported.")

        sprite = game_sprite.GameSprite(
            name=name,
            sprite_spec=sprite_spec,
            script=script,
        )
        sprite.center_x = start_location[0]
        sprite.center_y = start_location[1]

        self.scene.get_sprite_list(SCRIPTED_OBJECTS).append(sprite)

        if self.in_update:
            self.sprites_to_add[name] = sprite
        else:
            self._game_sprites[name] = sprite

        if is_first_load:
            script.on_start(sprite)

        script.set_api(self.api)
        script.set_owner(sprite)

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

        self.player_sprite.center_x = start[0].shape[0]  # type: ignore
        self.player_sprite.center_y = start[0].shape[1]  # type: ignore

    def _script_from_tiled_object(
        self,
        tiled_obj: arcade.TiledObject,
    ) -> scripts.Script:
        properties = tiled_obj.properties or {}

        try:
            return self._load_script(properties)
        except NoScript:
            return scripts.ObjectScript(
                self.api,
                on_activate=properties.get("on_activate"),
                on_activate_args=scripts.extract_script_args(
                    "on_activate_",
                    properties,
                ),
                on_hit=properties.get("on_hit"),
                on_hit_args=scripts.extract_script_args(
                    "on_hit_",
                    properties,
                ),
                on_collide=properties.get("on_collide"),
                on_collide_args=scripts.extract_script_args("on_collide_", properties),
                on_start=properties.get("on_start"),
                on_start_args=scripts.extract_script_args("on_start_", properties),
                on_tick=properties.get("on_tick"),
                on_tick_args=scripts.extract_script_args("on_tick_", properties),
            )

    def _load_script(self, properties: Dict[str, Any]) -> scripts.Script:
        if not "script" in properties:
            raise NoScript()

        cls = scripts.load_script_class(properties["script"])
        args = scripts.extract_script_args("script_", properties)
        obj = cls(**args)
        obj.set_api(self.api)
        return obj

    def on_update(self, delta_time: float) -> None:
        """Updates the model."""
        if self.physics_engine is None:
            raise SceneNotInitialized()

        self.in_update = True

        for sprite in self._game_sprites.values():
            if sprite.script is None:
                continue
            sprite.script.on_tick(self.sec_passed, delta_time)

        self.physics_engine.update(delta_time, on_collide=self._handle_collision)

        self._game_sprites.update(self.sprites_to_add)
        self.physics_engine.add_sprites(self.sprites_to_add.values())
        self.sprites_to_add = {}

        self.sec_passed += delta_time
        self.in_update = False

    def _handle_collision(
        self,
        sprite1: game_sprite.GameSprite,
        sprite2: game_sprite.GameSprite,
    ) -> None:
        obj1 = self._game_sprites.get(sprite1.name)
        if obj1 and obj1.script is not None:
            obj1.script.on_collide(obj1, sprite2)

        obj2 = self._game_sprites.get(sprite2.name)
        if obj2 and obj2.script is not None:
            obj2.script.on_collide(obj2, sprite1)

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

    def set_player_facing(self, facing_x: float, facing_y: float) -> None:
        """Sets the direction the player is facing."""
        self.player_sprite.facing_x = facing_x
        self.player_sprite.facing_y = facing_y

    def _objs_in_front_of_player(self) -> Iterable[game_sprite.GameSprite]:
        """get scripted obj in front of the player."""
        if self.scene is None:
            raise SceneNotInitialized()

        # Do a little bit of math to figure out where to place the hitbox.
        facing = pmath.Vec2(self.player_sprite.facing_x, self.player_sprite.facing_y)

        hitbox_center = facing.normalize().scale(HITBOX_DISTANCE)

        hitbox_corners = [
            (-HITBOX_DISTANCE, -HITBOX_DISTANCE),
            (HITBOX_DISTANCE, -HITBOX_DISTANCE),
            (HITBOX_DISTANCE, HITBOX_DISTANCE),
            (-HITBOX_DISTANCE, HITBOX_DISTANCE),
        ]
        hitbox_sprite = arcade.Sprite(
            center_x=hitbox_center.x + self.player_sprite.center_x,
            center_y=hitbox_center.y + self.player_sprite.center_y,
        )
        hitbox_sprite.set_hit_box(hitbox_corners)

        return cast(
            List[game_sprite.GameSprite],
            arcade.check_for_collision_with_list(
                hitbox_sprite,
                self.scene.get_sprite_list(SCRIPTED_OBJECTS),
            ),
        )

    def activate(self) -> None:
        """Activates whatever is in front of the player."""
        for obj in self._objs_in_front_of_player():
            if obj.script is None:
                continue
            obj.script.on_activate(obj, self.player_sprite)

    def hit(self) -> None:
        """Hit whatever is in front of the player."""
        for obj in self._objs_in_front_of_player():
            if obj.script is None:
                continue
            obj.script.on_hit(obj, self.player_sprite)

    def get_key_points(self, name: Optional[str]) -> List[scripts.KeyPoint]:
        """Queries for key points in the active region."""

        tilemap = self.tilemaps[self.active_region]

        key_points = []

        for point in tilemap.object_lists[KEY_POINTS]:
            if point.name is None:
                continue

            if name is not None and name not in point.name:
                continue

            shape = shapes.tiled_object_shape(point)
            key_points.append(
                scripts.KeyPoint(
                    name=point.name,
                    location=(shape.center_x, shape.center_y),
                    properties=point.properties or {},
                )
            )

        return key_points

    def get_sprites(self, name: Optional[str]) -> Iterable[game_sprite.GameSprite]:
        """Queries for sprites in the active region.

        Args:
            name: If set, acts as a substring filter for names.
        """

        if name is None:
            return self._game_sprites.values()

        return (sprite for sprite in self._game_sprites.values() if name in sprite.name)

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

    def draw(self) -> None:
        """Renders the model."""
        if self.scene is not None:
            self.scene.draw()
