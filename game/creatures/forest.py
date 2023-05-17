from typing import (
    List,
    Optional,
)

from game.scripts import (
    events,
    health,
    waypoints,
)
from engine import scripts

RAT_HEALTH = 10
RAT_DECAY_SECS = 10
RAT_DAMAGE = 1


class Rat(scripts.SavesOwner, health.DamagesPlayer, scripts.Script):
    """A rat creature."""

    _navigator: Optional[waypoints.Navigator]
    _waypoint_names: List[str]
    _health: health.Health
    _death_time: Optional[float]

    def __init__(self, **kwargs):
        """Constructs a new rat.

        Expected kwargs:
          waypoint_N - The names of waypoints that the rat will wander between.
                       The actual values of N don't matter, so long as they are
                       unique.
        """
        scripts.Script.__init__(self)
        health.DamagesPlayer.__init__(self, RAT_DAMAGE)
        self._navigator = None
        waypoint_args = [
            int(index)
            for index in scripts.extract_script_args(
                "waypoint_",
                kwargs,
            ).keys()
        ]
        self._waypoint_names = [kwargs[f"waypoint_{n}"] for n in waypoint_args]
        self._health = health.Health(initial_hp=RAT_HEALTH)
        self._death_time = None

    def on_hit(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        """Triggered when the player hits the rat."""
        assert self.api is not None

        if not self._health.is_dead:
            self._health.adjust(-self.api.player_data["base_damage"])

            if self._health.is_dead:
                self.api.fire_event(
                    events.CREATURE_KILLED,
                    events.CreatureKilled("rat"),
                )

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Handles game ticks."""
        if self.owner is None or self.api is None:
            return

        if self._health.is_dead:
            if self._death_time is None:
                self._death_time = game_time
                self.owner.speed = (0, 0)
                self.owner.custom_animation = "dead"
            elif self._death_time + RAT_DECAY_SECS < game_time:
                self.api.remove_sprite(self.owner.name)
            return

        if self._navigator is None:
            self._navigator = waypoints.Navigator(
                owner=self.owner,
                waypoints=[
                    next(iter(self.api.get_key_points(name)))
                    for name in self._waypoint_names
                ],
            )

        self._navigator.on_tick(game_time)
