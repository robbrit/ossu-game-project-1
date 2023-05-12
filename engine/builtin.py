"""This module defines a set of built-in scripts to be used from maps."""

import logging
import random
import sys
from typing import (
    Any,
    Callable,
    Dict,
    List,
)

from engine import scripts
from engine.model import game_sprite

logger = logging.Logger("engine.builtin")


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


def exit_game() -> None:
    """Exits the game."""
    sys.exit(0)


# Maximum number of spawns a spawner can have.
DEFAULT_NUM_SPAWNS = 1
# Percentage chance each second of spawning a creature if there is room to spawn.
DEFAULT_SPAWN_RATE_PER_SEC = 0.50
# Minimum amount of time between spawns.
DEFAULT_SPAWN_COOLDOWN_SECS = 10.0


class Spawner(scripts.SavesAPI, scripts.Script):
    """Class that handles spawning of creatures."""

    sprite_spec: str
    name: str
    spawn_script: Callable[[None], scripts.Script]
    spawn_script_kwargs: Dict[str, Any]
    num_spawns: int
    spawns: List[game_sprite.GameSprite]
    last_spawn: float
    spawn_rate_per_sec: float
    spawn_cooldown_secs: float
    id_counter: int

    def __init__(
        self,
        sprite_spec: str,
        name: str,
        spawn_script: str,
        num_spawns: int = DEFAULT_NUM_SPAWNS,
        spawn_rate_per_sec: float = DEFAULT_SPAWN_RATE_PER_SEC,
        spawn_cooldown_secs: float = DEFAULT_SPAWN_COOLDOWN_SECS,
        **kwargs,
    ):
        """Constructs a new spawner.

        Args:
            sprite_spec: the name of the sprite spec within the game spec.
            name: the name of this spawner. Must be unique to this region.
            spawn_script: the path to a callable that creates a Script object
                          for these sprites.
            num_spawns: the maximum number of spawns that this spawner can have
                        active at a time.
            spawn_rate_per_sec: probability of spawning a creature per second.
            spawn_cooldown_secs: wait this many seconds before spawning.

        Additional kwargs:
            spawn_script_X: kwargs passed to the spawn_script callable when it
                            is called.
        """
        super().__init__()

        self.sprite_spec = sprite_spec
        self.name = name
        self.spawn_script = scripts.load_script_class(spawn_script)
        self.spawn_script_kwargs = scripts.extract_script_args("spawn_script_", kwargs)
        self.num_spawns = num_spawns
        self.spawns = []
        self.last_spawn = float("-inf")
        self.spawn_rate_per_sec = spawn_rate_per_sec
        self.spawn_cooldown_secs = spawn_cooldown_secs
        self.id_counter = 0

    def on_start(self, owner: scripts.ScriptOwner):
        """Triggered the first time this spawn is created."""
        self._state["location"] = owner.location

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

    def _spawn(self):
        self.id_counter += 1

        logger.info("Spawner %s spawning %s", self.name, self.sprite_spec)

        sprite = self.api.create_sprite(
            spec_name=self.sprite_spec,
            name=f"{self.name}_spawn{self.id_counter}",
            start_location=self._state.get("location"),
            script=self.spawn_script(**self.spawn_script_kwargs),
        )
        self.spawns.append(sprite)
