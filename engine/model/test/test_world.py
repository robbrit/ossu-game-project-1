import unittest
from unittest import mock

import arcade

from engine.model import world
from engine.test import factories


@mock.patch("engine.model.game_sprite.GameSprite")
@mock.patch("arcade.load_tilemap")
@mock.patch("engine.model.player_sprite.PlayerSprite")
class CreateSpriteTest(unittest.TestCase):
    def test_cannot_add_existing_sprite(
        self,
        mocked_player,
        mocked_tilemap,
        mocked_game_sprite,
    ):
        # TODO(rob): Move all the mocking for Arcade into its own decorator.
        mock_tilemap = mock.Mock()
        mock_tilemap.object_lists = {
            "Key Points": [
                arcade.TiledObject(
                    name="Start",
                    shape=[0, 0],
                ),
            ],
        }
        mock_tilemap.sprite_lists = {
            "Wall Tiles": arcade.SpriteList(),
        }
        mock_tilemap.width = 10
        mock_tilemap.height = 10
        mock_tilemap.tile_width = 10
        mock_tilemap.tile_height = 10
        mocked_tilemap.return_value = mock_tilemap

        api = mock.Mock()
        sprite_spec = factories.fake_sprite_spec()
        spec = factories.fake_game_spec()

        w = world.World(api, spec, initial_player_data={})

        w.create_sprite(sprite_spec, "sprite", (0, 0), script=mock.Mock())

        with self.assertRaises(world.SpriteAlreadyExists):
            w.create_sprite(sprite_spec, "sprite", (0, 0), script=mock.Mock())


@mock.patch("engine.model.game_sprite.GameSprite")
@mock.patch("arcade.load_tilemap")
@mock.patch("engine.model.player_sprite.PlayerSprite")
class RemoveSpriteTest(unittest.TestCase):
    def test_cannot_add_existing_sprite(
        self,
        mocked_player,
        mocked_tilemap,
        mocked_game_sprite,
    ):
        # TODO(rob): Move all the mocking for Arcade into its own decorator.
        mock_tilemap = mock.Mock()
        mock_tilemap.object_lists = {
            "Key Points": [
                arcade.TiledObject(
                    name="Start",
                    shape=[0, 0],
                ),
            ],
        }
        mock_tilemap.sprite_lists = {
            "Wall Tiles": arcade.SpriteList(),
        }
        mock_tilemap.width = 10
        mock_tilemap.height = 10
        mock_tilemap.tile_width = 10
        mock_tilemap.tile_height = 10
        mocked_tilemap.return_value = mock_tilemap

        mocked_game_sprite.return_value.name = "sprite"

        api = mock.Mock()
        sprite_spec = factories.fake_sprite_spec()
        spec = factories.fake_game_spec()

        w = world.World(api, spec, initial_player_data={})

        w.create_sprite(sprite_spec, "sprite", (0, 0), script=mock.Mock())

        self.assertEqual(len(list(w.get_sprites(name="sprite"))), 1)

        w.remove_sprite("sprite")

        self.assertEqual(len(list(w.get_sprites(name="sprite"))), 0)
