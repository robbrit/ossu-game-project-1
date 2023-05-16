import dataclasses
import math
from os import path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

import arcade
import arcade.texture

from engine import (
    scripts,
    spec,
)


@dataclasses.dataclass
class Animation:
    """Wraps a set of information for a sprite animation."""

    spec: spec.AnimationSpec
    textures: List[arcade.texture.Texture]


class Animations:
    """Wraps all the details for animations."""

    # Mapping from animation name to the animation details.
    animations: Dict[str, Animation]
    # Name of the animation that is currently selected.
    current_animation: str
    # How much time we've spent in the current animation.
    time_index: float

    texture: arcade.Texture

    def __init__(self, sprite_spec: spec.GameSpriteSpec):
        self.animations = {
            name: Animation(
                spec=animation_spec,
                textures=arcade.load_spritesheet(
                    file_name=path.join(sprite_spec.root_directory, f"{name}.png"),
                    sprite_width=sprite_spec.width,
                    sprite_height=sprite_spec.height,
                    columns=animation_spec.num_frames,
                    count=animation_spec.num_frames,
                ),
            )
            for name, animation_spec in sprite_spec.animations.items()
        }
        self._reset_animation(sprite_spec.initial_animation)

    def _reset_animation(self, name: str) -> None:
        self.current_animation = name

        current_animation = self.animations[name]

        self.time_index = 0.0
        self.texture = current_animation.textures[0]

    def has_animation(self, name: str) -> bool:
        """Determines if the sequence has an animation with this name."""
        return name in self.animations

    def set_animation(self, name: str) -> None:
        """Changes the current animation for the sprite.

        Args:
            name: Which animation to show, as defined in the sprite's spec.

        Raises:
            KeyError: if there is no animation with that name.
        """
        if self.current_animation == name:
            return

        self._reset_animation(name)

    def update(self, delta_time: float):
        """Progresses the animation by a certain time step."""
        current_animation = self.animations[self.current_animation]
        sequence_duration = (
            len(current_animation.textures) * current_animation.spec.frame_speed
        )
        self.time_index = (self.time_index + delta_time) % sequence_duration
        current_frame = math.floor(self.time_index / current_animation.spec.frame_speed)

        self.texture = current_animation.textures[current_frame]


@dataclasses.dataclass
class SpriteState:
    """Wraps any persistable state for a sprite."""

    location: Tuple[float, float]
    facing: Tuple[float, float]
    data: Dict[str, Any]


class GameSprite(arcade.Sprite):
    """Wraps the various code related to sprites in our game.

    This includes support for animations, facing directions, etc.
    """

    _name: str

    _spec: Optional[spec.GameSpriteSpec]
    animations: Optional[Animations] = None
    script: Optional[scripts.Script] = None

    # X and Y directions that the character is facing.
    facing_x: float
    facing_y: float

    # Allows scripts to set a custom animation for this sprite.
    custom_animation: Optional[str]

    def __init__(
        self,
        name: str,
        sprite_spec: Optional[spec.GameSpriteSpec] = None,
        size: Optional[Tuple[float, float]] = None,
        script: Optional[scripts.Script] = None,
    ):
        width, height = 0.0, 0.0
        if size is not None:
            width, height = size
        elif sprite_spec is not None:
            width, height = sprite_spec.width, sprite_spec.height

        super().__init__(
            image_width=width,
            image_height=height,
        )
        self._name = name
        self.set_facing(x=1.0, y=1.0)
        self._spec = sprite_spec
        self.script = script
        self.custom_animation = None

        if sprite_spec is not None:
            self.animations = Animations(sprite_spec)
            self.texture = self.animations.texture

    def set_facing(self, x: float, y: float) -> None:
        """Sets the facing direction for the sprite."""
        self.facing_x = x
        self.facing_y = y

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Updates the sprite by a certain time step."""
        self._update_animation(delta_time)

    def _update_animation(self, delta_time: float) -> None:
        if self.animations is None:
            return

        animation = self._animation_state()
        direction = self._get_direction()

        key = f"{animation}-{direction}"

        if not self.animations.has_animation(key):
            key = animation

        self.animations.set_animation(key)
        self.animations.update(delta_time)
        self.texture = self.animations.texture

    def _animation_state(self) -> str:
        """Determines which 'animation state' we're in."""
        if self.custom_animation:
            return self.custom_animation

        if self.change_x != 0 or self.change_y != 0:
            return "walk"

        return "idle"

    def _get_direction(self) -> str:
        afx, afy = abs(self.facing_x), abs(self.facing_y)

        if afy > afx:
            return "up" if self.facing_y > 0 else "down"

        return "right" if self.facing_x > 0 else "left"

    @property
    def name(self) -> str:
        """Gets the name of this sprite."""
        return self._name

    @property
    def location(self) -> Tuple[float, float]:
        """Gets the location of this sprite.

        This is so that `GameSprite` adheres to the `ScriptOwner` protocol.
        """
        return (self.center_x, self.center_y)

    @property
    def speed(self) -> Tuple[float, float]:
        """Gets the speed of the script owner."""
        return (self.change_x, self.change_y)

    @speed.setter
    def speed(self, value: Tuple[float, float]) -> None:
        """Sets the speed of the script owner."""
        self.change_x, self.change_y = value
        self.facing_x, self.facing_y = value

        if self.facing_x == 0.0 and self.facing_y == 0.0:
            # Face down when not moving.
            self.facing_y = -1.0

    @property
    def state(self) -> SpriteState:
        """Gets the state of this sprite."""
        return SpriteState(
            location=(self.center_x, self.center_y),
            facing=(self.facing_x, self.facing_y),
            data=self.script.state if self.script is not None else {},
        )
