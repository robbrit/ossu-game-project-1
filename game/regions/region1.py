from engine import (
    builtin,
    scripts,
)
from engine.gui import conversation


class CoryCotton(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        assert self.api is not None
        self.api.show_gui(CoryCottonChat())


class AdeleCotton(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        assert self.api is not None
        self.api.show_gui(AdeleCottonChat())


class LouisMckay(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        assert self.api is not None
        self.api.show_gui(LouisMckayChat())


class CoryCottonChat(conversation.GUI):
    def __init__(self):
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
                choices=[holden],
            ),
        )
        holden.link.choices = [forest]

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
                ],
            )
        )


class AdeleCottonChat(conversation.GUI):
    def __init__(self):
        cory = conversation.Choice(
            text="Cory",
            link=conversation.Conversation(
                text="That's my husband. He's standing over there.",
                choices=[],
            ),
        )

        super().__init__(
            conversation.Conversation(
                title="Adele Cotton",
                text=("Hello, my name is Adele. I live here with my husband Cory."),
                choices=[
                    cory,
                ],
            )
        )


class LouisMckayChat(conversation.GUI):
    def __init__(self):
        super().__init__(
            conversation.Conversation(
                title="Louis Mckay",
                text="Welcome to my shop.",
                choices=[],
            )
        )
