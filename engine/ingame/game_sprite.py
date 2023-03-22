import json
from os import path
from typing import (
    Dict,
    List,
    NamedTuple,
)

import arcade
import arcade.texture


class GameSpriteSpec(NamedTuple):
    """This spec wraps the format of the JSON files that define a sprite's animation."""

    width: int
    height: int
    fps: float

    initial_animation: str
    root_directory: str
    animation_names: List[str]


class GameSprite(arcade.Sprite):
    """Wraps the various code related to sprites in our game.

    This includes support for animations, facing directions, etc.
    """

    animations: Dict[str, arcade.texture.Texture]
    current_animation: str
    spec: GameSpriteSpec

    num_frames: int
    current_frame: int
    time_index: float

    def __init__(self, spec_filename: str):
        with open(spec_filename) as f:
            data = json.loads(f.read())
            spec = GameSpriteSpec(**data)

        super().__init__(image_width=spec.width, image_height=spec.height)

        self.spec = spec
        self.animations = {
            name: arcade.load_texture(path.join(spec.root_directory, f"{name}.png"))
            for name in spec.animation_names
        }
        self.current_animation = ""
        self.set_animation(spec.initial_animation)
        self.time_index = 0.0

    def set_animation(self, name: str) -> None:
        if self.current_animation == name:
            return

        self.current_animation = name
        self.texture = self.animations[name]
        self.image_width = self.spec.width
        self.image_height = self.spec.height

        self.num_frames = self.texture.width / self.spec.width
        self.time_index = 0.0
        self.current_frame = 0

    def update_animation(self, dt: float) -> None:
        self.time_index = (self.time_index + dt) % (self.num_frames / self.spec.fps)
        self.current_frame = (self.time_index / self.spec.fps) % self.num_frames

        self.image_x = self.spec.width * self.current_frame

    def on_update(self, dt: float) -> None:
        if self.change_x != 0 or self.change_y != 0:
            self.set_animation("walk")
        else:
            self.set_animation("idle")

        self.update_animation(dt)
