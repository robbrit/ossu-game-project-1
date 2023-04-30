import unittest
from unittest import mock

from engine.model import player_sprite


class PlayerSpriteTest(unittest.TestCase):
    def test_activate_animation(self):
        api = mock.Mock()
        api.current_time_secs = 17.0

        player = player_sprite.PlayerSprite(api, sprite_spec=None, initial_state={})
        self.assertEqual(player._animation_state(), "idle")

        player.on_activate()
        self.assertEqual(player._animation_state(), "activate")
        api.current_time_secs += 0.1
        self.assertEqual(player._animation_state(), "activate")
        api.current_time_secs += 0.4
        self.assertEqual(player._animation_state(), "idle")
