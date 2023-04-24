from engine import (
    builtin,
    scripts,
)
from engine.gui import conversation


class CoryCotton(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        self.api.show_gui(CoryCottonChat())


class LouisMckay(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        self.api.show_gui(LouisMckayChat())


class CoryCottonChat(conversation.GUI):
    def __init__(self):
        bye = conversation.Choice(
            text="Bye!",
            action=builtin.resume_game,
        )

        holden = conversation.Choice(
            text="Holden",
            link=conversation.Conversation(
                text=(
                    "This is a small town named Holden, just a few of us living here now. There's "
                    "a shop next to me run by my friend Louis, go ahead and run inside if you "
                    "haven't already."
                ),
                choices=[],
            ),
        )

        forest = conversation.Choice(
            text="Forest",
            link=conversation.Conversation(
                text=(
                    "There's a forest to the west. It's dangerous, be sure to pick up some way to "
                    "defend yourself if you want to go out there."
                ),
                choices=[holden, bye],
            ),
        )
        holden.link.choices = [forest, bye]

        super().__init__(
            conversation.Conversation(
                title="Cory Cotton",
                text=(
                    "Welcome! My name is Cory, and this town is Holden. You can ask me "
                    "about anything!"
                ),
                choices=[
                    holden,
                    forest,
                    bye,
                ],
            )
        )


class LouisMckayChat(conversation.GUI):
    def __init__(self):
        super().__init__(
            conversation.Conversation(
                title="Louis Mckay",
                text="Welcome to my shop.",
                # TODO(rob): Create a "shop" GUI that we can plug in here.
                choices=[
                    conversation.Choice(
                        text="Bye!",
                        action=builtin.resume_game,
                    ),
                ],
            )
        )
