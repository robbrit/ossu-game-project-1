from engine import core

from game.gui import start


def run() -> None:
    core.Core(
        initial_gui=start.StartScreen(),
    ).run()
