"""This module defines a set of built-in scripts to be used from maps."""

from engine import scripts


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
