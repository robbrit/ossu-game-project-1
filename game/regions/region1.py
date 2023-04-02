from engine import scripts
from engine.gui import conversation


def building1_door(api: scripts.GameAPI) -> None:
    api.change_region("Region1Building1", "Entryway")


def building1_exit(api: scripts.GameAPI) -> None:
    api.change_region("Region1", "Building 1 Exit")


class IntroCharacter(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        self.api.show_gui(TalkToNPC())


class TalkToNPC(conversation.GUI):
    def __init__(self):
        # TODO(rob): Add a choice that goes back to the game. In order to do that we
        # need to start_game() resume the game instead of restarting it.
        super().__init__(
            conversation.Conversation(
                title="Chat with random dude",
                text="Welcome!",
                choices=[
                    conversation.Choice(
                        text="Hi",
                        link=conversation.Conversation(
                            text="Hi!",
                            choices=[],
                        ),
                    )
                ],
            )
        )
