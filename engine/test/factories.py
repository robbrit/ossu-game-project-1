"""This module defines a set of factory functions to generate data for tests."""

import dataclasses

from engine import spec


def fake_region_spec(**args) -> spec.RegionSpec:
    """Constructs a fake RegionSpec."""
    defaults = {
        "tiled_mapfile": "",
    }
    defaults.update(args)
    return spec.RegionSpec(**defaults)


def fake_world_spec(**args) -> spec.WorldSpec:
    """Constructs a fake WorldSpec."""
    defaults = {
        "regions": {
            "region1": fake_region_spec(),
        },
        "initial_region": "region1",
    }
    defaults.update(args)
    return spec.WorldSpec(**defaults)


def fake_animation_spec(**args) -> spec.AnimationSpec:
    """Constructs a fake AnimationSpec."""
    defaults = {
        "num_frames": 1,
        "frame_speed": 1.0,
    }
    defaults.update(args)
    return spec.AnimationSpec(**defaults)


def fake_sprite_spec(**args) -> spec.GameSpriteSpec:
    """Constructs a fake GameSpriteSpec."""
    defaults = {
        "width": 10,
        "height": 10,
        "initial_animation": "idle",
        "root_directory": "",
        "animations": {
            "idle": dataclasses.asdict(fake_animation_spec()),
        },
    }
    defaults.update(**args)
    return spec.GameSpriteSpec(**defaults)


def fake_game_spec(**args) -> spec.GameSpec:
    """Constructs a fake GameSpec."""
    defaults = {
        "world": dataclasses.asdict(fake_world_spec(**args.get("world", {}))),
        "player_spec": dataclasses.asdict(fake_sprite_spec(**args.get("player", {}))),
        "sprites": {},
        "guis": {},
        "sounds": {},
    }

    for key in ["world", "player_spec"]:
        if key in args:
            del args[key]

    defaults.update(args)
    return spec.GameSpec(**defaults)
