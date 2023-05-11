from typing import (
    Callable,
    Iterable,
    List,
    Tuple,
)

import arcade

from engine.model import game_sprite


class Engine:
    """Our implementation of a physics engine."""

    moveable_sprites: List[game_sprite.GameSprite]
    wall_sprite_list: arcade.SpriteList
    map_size: Tuple[float, float]

    def __init__(
        self,
        moveable_sprites: Iterable[game_sprite.GameSprite],
        wall_sprite_list: arcade.SpriteList,
        map_size: Tuple[float, float],
    ):
        """Constructs a new physics engine.

        Args:
            moveable_sprites: A set of sprites to have the physics engine manage. Any
                              sprite will be moved according to its change_* speeds.
                              All sprites will collide with walls or the edge of the
                              world, and any collisions between two sprites that both
                              have a truthy "solid" property will not move.
            wall_sprite_list: A sprite list representing immoveable wall tiles.
            map_size: The size of the map in pixels.
        """

        self.moveable_sprites = list(moveable_sprites)
        self.wall_sprite_list = wall_sprite_list
        self.map_size = map_size

    def add_sprites(self, sprites: Iterable[game_sprite.GameSprite]) -> None:
        """Adds a number of sprites to the engine."""
        self.moveable_sprites.extend(sprites)

    def remove_sprite(self, name: str) -> None:
        """Removes a sprite from the physics engine."""
        self.moveable_sprites = [
            sprite for sprite in self.moveable_sprites if sprite.name != name
        ]

    def update(
        self,
        delta_time: float,
        on_collide: Callable[[game_sprite.GameSprite, game_sprite.GameSprite], None],
    ) -> None:
        """Updates all objects in the physics engine."""

        self._move_sprites(delta_time, on_collide)

        for sprite in self.moveable_sprites:
            sprite.on_update(delta_time)

    def _move_sprites(
        self,
        delta_time: float,
        on_collide: Callable[[game_sprite.GameSprite, game_sprite.GameSprite], None],
    ) -> None:
        collisions = set()

        original_positions = [
            (sprite.center_x, sprite.center_y) for sprite in self.moveable_sprites
        ]

        # First, check against walls.
        for i, sprite in enumerate(self.moveable_sprites):
            if sprite.change_x != 0:
                sprite.center_x += sprite.change_x * delta_time

                if self._collides_with_wall(sprite) or self._is_oob(sprite):
                    sprite.center_x = original_positions[i][0]

            if sprite.change_y != 0:
                sprite.center_y += sprite.change_y * delta_time

                if self._collides_with_wall(sprite) or self._is_oob(sprite):
                    sprite.center_y = original_positions[i][1]

        # Now check against other moving sprites.
        sprites_to_revert = set()

        for i, sprite1 in enumerate(self.moveable_sprites):
            is_solid = sprite1.properties.get("solid", False)
            for j in range(i + 1, len(self.moveable_sprites)):
                sprite2 = self.moveable_sprites[j]
                if arcade.check_for_collision(sprite1, sprite2):
                    if is_solid or sprite2.properties.get("solid", False):
                        sprites_to_revert.add(i)
                        sprites_to_revert.add(j)
                    collisions.add((i, j))

        for idx in sprites_to_revert:
            sprite = self.moveable_sprites[idx]
            sprite.center_x, sprite.center_y = original_positions[idx]

        for idx1, idx2 in collisions:
            on_collide(self.moveable_sprites[idx1], self.moveable_sprites[idx2])

    def _collides_with_wall(self, sprite: game_sprite.GameSprite) -> bool:
        collisions = arcade.check_for_collision_with_list(sprite, self.wall_sprite_list)
        return len(collisions) > 0

    def _is_oob(self, sprite: game_sprite.GameSprite) -> bool:
        if sprite.center_x < 0 or sprite.center_x >= self.map_size[0]:
            return True

        return sprite.center_y < 0 or sprite.center_y >= self.map_size[1]
