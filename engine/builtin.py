"""This module defines a set of built-in scripts to be used from maps."""

import random
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
)

from engine import scripts
from engine.model import game_sprite


def transition_region(api: scripts.GameAPI, region: str, start_location: str) -> None:
    """Transitions the game to a different region.

    Args:
        api: The game API object.
        region: The name of the region to transition to, as defined in the game spec.
        start_location: The name of the point in the target region where the player will
                        appear when the transition is complete.
    """
    api.change_region(region, start_location)


def resume_game(api: scripts.GameAPI) -> None:
    """Starts/resumes the game."""
    api.start_game()


# Maximum number of spawns a spawner can have.
DEFAULT_NUM_SPAWNS = 1
# Percentage chance each second of spawning a creature if there is room to spawn.
DEFAULT_SPAWN_RATE_PER_SEC = 0.20
# Minimum amount of time between spawns.
DEFAULT_SPAWN_COOLDOWN_SECS = 10.0


class Spawner(scripts.Script, scripts.SavesAPI):
    """Class that handles spawning of creatures."""

    spawner_cls: Type[game_sprite.GameSprite]
    location: Optional[Tuple[float, float]]
    num_spawns: int
    spawns: List[game_sprite.GameSprite]
    last_spawn: float
    spawn_rate_per_sec: float
    spawn_cooldown_secs: float

    def __init__(
        self,
        spawner_cls: str,
        num_spawns: int = DEFAULT_NUM_SPAWNS,
        spawn_rate_per_sec: float = DEFAULT_SPAWN_RATE_PER_SEC,
        spawn_cooldown_secs: float = DEFAULT_SPAWN_COOLDOWN_SECS,
    ):
        super().__init__()

        self.spawner_cls = scripts.load_symbol(spawner_cls)
        self.location = None
        self.num_spawns = num_spawns
        self.spawns = []
        self.last_spawn = float("-inf")
        self.spawn_rate_per_sec = spawn_rate_per_sec
        self.spawn_cooldown_secs = spawn_cooldown_secs

    def on_start(self, owner: scripts.ScriptOwner):
        """Triggered the first time this spawn is created."""
        self.location = owner.location

    def _can_spawn(self, now: float) -> bool:
        return (
            len(self.spawns) < self.num_spawns
            and self.last_spawn + self.spawn_cooldown_secs < now
        )

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Occasionally spawns a creature."""
        # Use a pretty simple extrapolation method to map the per-second probability to
        # match the delta.
        probability = min(1.0, self.spawn_rate_per_sec * delta_time)

        if self._can_spawn(game_time) and random.random() < probability:
            self._spawn()

    @property
    def state(self) -> Dict[str, Any]:
        """Gets the state of this spawner."""
        # TODO(rob): Need some way to reference any existing spawns so that when we
        # reload, we can rebuild those references.
        return {}

    @state.setter
    def state(self, state: Dict[str, Any]) -> None:
        """Sets the state of this spawner."""

    def _spawn(self):
        print("Spawn")
