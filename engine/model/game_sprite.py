import dataclasses
import math
from os import path
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import arcade
import arcade.texture

from engine import (
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
    # How much time we we've spent in the current animation.
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


class GameSprite(arcade.Sprite):
    """Wraps the various code related to sprites in our game.

    This includes support for animations, facing directions, etc.
    """

    # The spec for this sprite.
    _spec: spec.GameSpriteSpec
    animations: Optional[Animations]

    # X and Y directions that the character is facing.
    facing_x: float
    facing_y: float

    def __init__(
        self,
        sprite_spec: spec.GameSpriteSpec,
    ):
        super().__init__(image_width=sprite_spec.width, image_height=sprite_spec.height)
        self.set_facing(x=1.0, y=1.0)
        self._spec = sprite_spec
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

        try:
            self.animations.set_animation(f"{animation}-{direction}")
        except KeyError:
            # This is possibly becase they don't have directional animations. If they
            # don't, just use the base animation.
            self.animations.set_animation(animation)

        self.animations.update(delta_time)
        self.texture = self.animations.texture

    def _animation_state(self) -> str:
        """Determines which 'animation state' we're in."""
        if self.change_x != 0 or self.change_y != 0:
            return "walk"

        return "idle"

    def _get_direction(self) -> str:
        # TODO(rob): Should probably do an enum for facing direction.
        afx, afy = abs(self.facing_x), abs(self.facing_y)

        if afy > afx:
            return "up" if self.facing_y > 0 else "down"

        return "right" if self.facing_x > 0 else "left"

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
