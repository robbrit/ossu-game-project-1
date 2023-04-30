import unittest
from unittest import mock

from pyglet import math as pmath

from engine.ingame import view

CAMERA_SIZE = 200


class InGameViewTest(unittest.TestCase):
    def create_world(self):
        world = mock.Mock()
        world.player_sprite = mock.Mock()
        world.tile_width = 32
        world.tile_height = 32
        world.width = 100
        world.height = 100
        return world

    def create_camera(self):
        return mock.Mock(viewport_width=CAMERA_SIZE, viewport_height=CAMERA_SIZE)

    @mock.patch("arcade.Camera")
    def test_normal_camera_centering(self, mock_camera):
        camera = self.create_camera()
        mock_camera.return_value = camera

        world = self.create_world()

        world.player_sprite.center_x = 500
        world.player_sprite.center_y = 500

        game_view = view.InGameView(world, (CAMERA_SIZE, CAMERA_SIZE), gui=None)
        game_view.on_update(1.0)
        # The player should be in the center of the camera, so the camera should be
        # offset by half the viewport size.
        camera.move_to.assert_called_with(
            pmath.Vec2(500 - CAMERA_SIZE / 2, 500 - CAMERA_SIZE / 2),
        )

    @mock.patch("arcade.Camera")
    def test_camera_centering_edges(self, mock_camera):
        camera = self.create_camera()
        mock_camera.return_value = camera

        for player_x, player_y, camera_x, camera_y in [
            (5, 500, 0, 500 - CAMERA_SIZE / 2),  # Left
            (3200 - 5, 500, 3200 - CAMERA_SIZE, 500 - CAMERA_SIZE / 2),  # Right
            (500, 3200 - 5, 500 - CAMERA_SIZE / 2, 3200 - CAMERA_SIZE),  # Top
            (500, 5, 500 - CAMERA_SIZE / 2, 0),  # Bottom
        ]:
            world = self.create_world()

            world.player_sprite.center_x = player_x
            world.player_sprite.center_y = player_y

            game_view = view.InGameView(world, (CAMERA_SIZE, CAMERA_SIZE), gui=None)
            game_view.on_update(1.0)
            camera.move_to.assert_called_with(pmath.Vec2(camera_x, camera_y))

    @mock.patch("arcade.Camera")
    def test_camera_centering_thin_world(self, mock_camera):
        camera = self.create_camera()
        mock_camera.return_value = camera

        small_offset = (5 * 32 - CAMERA_SIZE) / 2

        for world_width, world_height, player_x, player_y, camera_x, camera_y in [
            # Small height
            (10000, 5, 2000, 90, 2000 - CAMERA_SIZE / 2, small_offset),
            # Small width
            (5, 10000, 90, 2000, small_offset, 2000 - CAMERA_SIZE / 2),
            # Both small
            (5, 5, 90, 90, small_offset, small_offset),
        ]:
            world = self.create_world()
            world.width = world_width
            world.height = world_height

            world.player_sprite.center_x = player_x
            world.player_sprite.center_y = player_y

            game_view = view.InGameView(world, (CAMERA_SIZE, CAMERA_SIZE), gui=None)
            game_view.on_update(1.0)
            camera.move_to.assert_called_with(pmath.Vec2(camera_x, camera_y))
