from typing import (
    List,
)

from engine import scripts


class Rat(scripts.Script):
    """A rat creature."""

    waypoints: List[str]
    current_waypoint: int

    def __init__(self, **kwargs):
        """Constructs a new rat.

        Expected kwargs:
          waypoint_N - The names of waypoints that the rat will wander between.
                       The actual values of N don't matter, so long as they are
                       unique.
        """
        waypoint_args = [
            int(index)
            for index in scripts.extract_script_args("waypoint_", kwargs).keys()
        ]
        self.waypoints = [kwargs[f"waypoint_{n}"] for n in waypoint_args]
        self.current_waypoint = 0

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Handles game ticks."""
