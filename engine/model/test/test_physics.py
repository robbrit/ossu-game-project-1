from typing import (
    Iterable,
    Tuple,
)
import unittest
from unittest import mock

import arcade

from engine.model import (
    physics,
)


@mock.patch("arcade.check_for_collision_with_list")
class PhysicsTest(unittest.TestCase):
    def test_collide_with_wall(self, mock_collide):
        wall_list = arcade.SpriteList()
        wall_sprite = arcade.Sprite()
        wall_list.append(wall_sprite)

        # Make the mock say there is no collision in the X direction, but there is one
        # in the Y direction.
        mock_collide.side_effect = [[], [wall_sprite]]

        player = arcade.Sprite()
        player.center_x = 11
        player.center_y = 11
        player.change_x = 2
        player.change_y = -2

        engine = physics.Engine(
            [player],
            wall_list,
            map_size=(100, 100),
        )
        engine.update(1.0, lambda c1, c2: None)

        self.assertEqual(player.center_x, 13)
        self.assertEqual(player.center_y, 11)

    def test_collide_with_oob(self, mock_collide):
        wall_list = arcade.SpriteList()

        mock_collide.return_value = []

        # Check in the X direction.
        player = arcade.Sprite()
        player.center_x = 1
        player.center_y = 1
        player.change_x = -2
        player.change_y = 0

        engine = physics.Engine(
            [player],
            wall_list,
            map_size=(100, 100),
        )
        engine.update(1.0, lambda c1, c2: None)

        self.assertEqual(player.center_x, 1)
        self.assertEqual(player.center_y, 1)

        # Check in the Y direction.
        player = arcade.Sprite()
        player.center_x = 1
        player.center_y = 1
        player.change_x = 0
        player.change_y = -2

        engine = physics.Engine(
            [player],
            wall_list,
            map_size=(100, 100),
        )
        engine.update(1.0, lambda c1, c2: None)

        self.assertEqual(player.center_x, 1)
        self.assertEqual(player.center_y, 1)

    @mock.patch("arcade.check_for_collision")
    def test_collide_with_solid(self, mock_collide_sprite, mock_collide_list):
        wall_list = arcade.SpriteList()

        mock_collide_list.return_value = []
        mock_collide_sprite.return_value = True

        sprite1 = arcade.Sprite()
        sprite1.center_x = 1
        sprite1.center_y = 1
        sprite1.change_x = 2
        sprite1.change_y = 0
        sprite1.properties = {"solid": True}

        sprite2 = arcade.Sprite()
        sprite2.center_x = 3
        sprite2.center_y = 1
        sprite2.change_x = -2
        sprite2.change_y = 0
        sprite2.properties = {"solid": True}

        called = False

        def collision(s1, s2):
            nonlocal called
            called = True
            self.assertEqual(s1, sprite1)
            self.assertEqual(s2, sprite2)

        engine = physics.Engine(
            [sprite1, sprite2],
            wall_list,
            map_size=(100, 100),
        )
        engine.update(1.0, collision)

        self.assertEqual(sprite1.center_x, 1)
        self.assertEqual(sprite1.center_y, 1)
        self.assertEqual(sprite2.center_x, 3)
        self.assertEqual(sprite2.center_y, 1)
        self.assertTrue(called)

    @mock.patch("arcade.check_for_collision")
    def test_collide_with_solid(self, mock_collide_sprite, mock_collide_list):
        wall_list = arcade.SpriteList()

        mock_collide_list.return_value = []
        mock_collide_sprite.return_value = True

        sprite1 = arcade.Sprite()
        sprite1.center_x = 1
        sprite1.center_y = 1
        sprite1.change_x = 2
        sprite1.change_y = 0
        sprite1.properties = {"solid": False}

        sprite2 = arcade.Sprite()
        sprite2.center_x = 3
        sprite2.center_y = 1
        sprite2.change_x = -2
        sprite2.change_y = 0
        sprite2.properties = {"solid": False}

        called = False

        def collision(s1, s2):
            nonlocal called
            called = True
            self.assertEqual(s1, sprite1)
            self.assertEqual(s2, sprite2)

        engine = physics.Engine(
            [sprite1, sprite2],
            wall_list,
            map_size=(100, 100),
        )
        engine.update(1.0, collision)

        self.assertEqual(sprite1.center_x, 3)
        self.assertEqual(sprite1.center_y, 1)
        self.assertEqual(sprite2.center_x, 1)
        self.assertEqual(sprite2.center_y, 1)
        self.assertTrue(called)
