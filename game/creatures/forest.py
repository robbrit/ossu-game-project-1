from typing import (
    List,
    Optional,
)

from game.scripts import waypoints
from engine import scripts


class Rat(scripts.SavesAPI, scripts.SavesOwner, scripts.Script):
    """A rat creature."""

    _navigator: Optional[waypoints.Navigator]
    _waypoint_names: List[str]

    def __init__(self, **kwargs):
        """Constructs a new rat.

        Expected kwargs:
          waypoint_N - The names of waypoints that the rat will wander between.
                       The actual values of N don't matter, so long as they are
                       unique.
        """
        super(scripts.Script, self).__init__()
        self._navigator = None
        waypoint_args = [
            int(index)
            for index in scripts.extract_script_args(
                "waypoint_",
                kwargs,
            ).keys()
        ]
        self._waypoint_names = [kwargs[f"waypoint_{n}"] for n in waypoint_args]

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Handles game ticks."""
        if self.owner is None or self.api is None:
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
