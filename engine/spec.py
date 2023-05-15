import dataclasses
from typing import (
    Any,
    Dict,
    Optional,
)

from engine.gui import widgets


@dataclasses.dataclass
class AnimationSpec:
    """This spec describes a single animation for a sprite."""

    num_frames: int
    frame_speed: float  # Number of seconds each frame should be shown for.


@dataclasses.dataclass
class _GameSpriteSpecBase:
    """Base class for GameSpriteSpec so we don't have to write a ton of code."""

    width: int
    height: int

    initial_animation: str
    root_directory: str
    animations: Dict[str, AnimationSpec]


class GameSpriteSpec(_GameSpriteSpecBase):
    """This spec wraps the format of the JSON files that define a sprite's animation."""

    def __init__(self, **kwargs):
        kwargs["animations"] = {
            name: AnimationSpec(**a) for name, a in kwargs.get("animations", {}).items()
        }
        super().__init__(**kwargs)


@dataclasses.dataclass
class RegionSpec:
    """Specifies the details of a particular region."""

    tiled_mapfile: str
    wall_layer: str = "Wall Tiles"


@dataclasses.dataclass
class WorldSpec:
    """Specifies the details for the entire world."""

    regions: Dict[str, RegionSpec]
    initial_region: str

    # TODO(rob): Hit/activate sounds would be better off as scripts listening for
    # events, see #140.
    hit_sound: Optional[str]
    activate_sound: Optional[str]

    def __init__(
        self,
        regions: Dict[str, Any],
        initial_region: str,
        hit_sound: Optional[str] = None,
        activate_sound: Optional[str] = None,
    ):
        self.regions = {
            region_name: r if isinstance(r, RegionSpec) else RegionSpec(**r)
            for region_name, r in regions.items()
        }
        self.initial_region = initial_region
        self.hit_sound = hit_sound
        self.activate_sound = activate_sound


@dataclasses.dataclass
class SoundSpec:
    """Contains configuration details for a sound."""

    path: str

    # Allow streaming the file from disk. This saves memory, but is slow to load. Use it
    # for longer sounds like music.
    stream: bool = False


@dataclasses.dataclass
class GameSpec:
    """Contains all the configuration details for the entire game."""

    world: WorldSpec
    player_spec: GameSpriteSpec
    sprites: Dict[str, GameSpriteSpec]
    guis: Dict[str, widgets.GUISpec]
    sounds: Dict[str, SoundSpec]

    def __init__(
        self,
        world: Dict[str, Any],
        player_spec: Dict[str, Any],
        sprites: Dict[str, Any],
        guis: Dict[str, Any],
        sounds: Dict[str, Any],
    ):
        self.world = WorldSpec(**world)
        self.player_spec = GameSpriteSpec(**player_spec)
        self.sprites = {name: GameSpriteSpec(**spec) for name, spec in sprites.items()}
        self.guis = {name: widgets.GUISpec(**spec) for name, spec in guis.items()}
        self.sounds = {name: SoundSpec(**spec) for name, spec in sounds.items()}
