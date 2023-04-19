from engine import scripts


class Rat(scripts.Script):
    """A rat creature."""

    def on_tick(self, game_time: float, delta_time: float) -> None:
        """Handles game ticks."""
