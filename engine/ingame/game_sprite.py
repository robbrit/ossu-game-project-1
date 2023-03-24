import json
import math
from os import path
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
)

import arcade
import arcade.texture


class AnimationSpec(NamedTuple):
    """This spec describes a single animation for a sprite."""

    num_frames: int
    frame_speed: float  # Number of seconds each frame should be shown for.


class GameSpriteSpec(NamedTuple):
    """This spec wraps the format of the JSON files that define a sprite's animation."""

    width: int
    height: int

    initial_animation: str
    root_directory: str
    animations: Dict[str, AnimationSpec]

    @classmethod
    def create(cls, data: Dict[str, Any]) -> "GameSpriteSpec":
        data = data.copy()
        data["animations"] = {
            name: AnimationSpec(**a) for name, a in data["animations"].items()
        }

        return GameSpriteSpec(**data)


class Animation(NamedTuple):
    """Wraps a set of information for a sprite animation."""

    spec: AnimationSpec
    textures: List[arcade.texture.Texture]


class GameSprite(arcade.Sprite):
    """Wraps the various code related to sprites in our game.

    This includes support for animations, facing directions, etc.
    """

    # Mapping from animation name to the animation details.
    animations: Dict[str, Animation]
    # Name of the animation that is currently selected.
    current_animation: Optional[str]
    # The spec for this sprite.
    spec: GameSpriteSpec

    # How much time we we've spent in the current animation.
    time_index: float

    # X and Y directions that the character is facing.
    facing_x: float
    facing_y: float

    def __init__(self, spec_filename: str):
        with open(spec_filename) as f:
            data = json.loads(f.read())
            spec = GameSpriteSpec.create(data)

        super().__init__(image_width=spec.width, image_height=spec.height)

        self.set_facing(x=1.0, y=1.0)

        self.spec = spec
        self.animations = {
            name: Animation(
                spec=animation_spec,
                textures=arcade.load_spritesheet(
                    file_name=path.join(spec.root_directory, f"{name}.png"),
                    sprite_width=spec.width,
                    sprite_height=spec.height,
                    columns=animation_spec.num_frames,
                    count=animation_spec.num_frames,
                ),
            )
            for name, animation_spec in spec.animations.items()
        }
        self.current_animation = None
        self.set_animation(spec.initial_animation)

    def set_facing(self, x: float, y: float) -> None:
        """Sets the facing direction for the sprite."""
        self.facing_x = x
        self.facing_y = y

    def set_animation(self, name: str) -> None:
        """Changes the current animation for the sprite.

        Args:
            name: Which animation to show, as defined in the sprite's spec.

        Raises:
            KeyError: if there is no animation with that name.
        """
        if self.current_animation == name:
            return

        self.current_animation = name

        current_animation = self.animations[name]

        self.time_index = 0.0
        self.texture = current_animation.textures[0]

    def update_animation(self, dt: float) -> None:
        """Progresses the animation by a certain time step."""
        current_animation = self.animations[self.current_animation]
        sequence_duration = (
            len(current_animation.textures) * current_animation.spec.frame_speed
        )
        self.time_index = (self.time_index + dt) % sequence_duration
        current_frame = math.floor(self.time_index / current_animation.spec.frame_speed)

        self.texture = current_animation.textures[current_frame]

    def on_update(self, dt: float) -> None:
        """Updates the sprite by a certain time step."""
        moving = self.change_x != 0 or self.change_y != 0

        animation = "walk" if moving else "idle"
        direction = self._get_direction()

        self.set_animation(f"{animation}-{direction}")
        self.update_animation(dt)

    def _get_direction(self) -> str:
        # TODO(rob): Should probably do an enum for facing direction.
        fx, fy = self.facing_x, self.facing_y
        afx, afy = abs(fx), abs(fy)

        if afy > afx:
            return "up" if fy > 0 else "down"

        return "right" if fx > 0 else "left"
