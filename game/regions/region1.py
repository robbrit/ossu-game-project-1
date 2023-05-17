from engine import (
    scripts,
)
from engine.gui import conversation

from game.quests import (
    base as quests,
    db as quests_db,
    region1 as region1_quests,
)


class CoryCotton(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        assert self.api is not None
        self.api.show_gui(CoryCottonChat())


class AdeleCotton(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        assert self.api is not None

        # TODO(rob): Check the quest completion condition here.

        self.api.show_gui(AdeleCottonChat())


class LouisMckay(scripts.SavesAPI, scripts.Script):
    def on_activate(self, owner: scripts.ScriptOwner, player: scripts.Player) -> None:
        assert self.api is not None
        self.api.show_gui(LouisMckayChat())


class CoryCottonChat(conversation.GUI):
    def __init__(self):
        holden = conversation.Choice(
            text="Holden",
            link=conversation.StaticConversation(
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
            link=conversation.StaticConversation(
                text=(
                    "There's a forest to the west. It's dangerous, be sure to pick up some way to "
                    "defend yourself if you want to go out there."
                ),
                choices=[holden],
            ),
        )
        holden.link.choices = [forest]

        super().__init__(
            conversation.StaticConversation(
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
            link=conversation.StaticConversation(
                text="That's my husband. He's standing over there.",
                choices=[],
            ),
        )

        help = conversation.Choice(
            text="Help",
            condition=self._show_help_choice,
            link=conversation.StaticConversation(
                text=(
                    "I have a problem with rats in my garden. They sneak in from the "
                    "forest to the west and eat my tomatoes. Can you go in and "
                    "kill a few of them for me?"
                ),
                choices=[
                    conversation.Choice(
                        text="Sure!",
                        action=self._accept_quest,
                        link=conversation.StaticConversation(
                            text="Thank you so much!",
                            choices=[cory],
                        ),
                    ),
                    conversation.Choice(
                        text="No thanks.",
                        action=self._reject_quest,
                        link=conversation.StaticConversation(
                            text="That's a shame. I'll have to find someone else.",
                            choices=[cory],
                        ),
                    ),
                ],
            ),
        )

        super().__init__(
            conversation.StaticConversation(
                title="Adele Cotton",
                text=self._initial_text,
                choices=[cory, help],
            )
        )

    def _show_help_choice(self, api: scripts.GameAPI) -> bool:
        quest = quests_db.get_state(api, region1_quests.KILL_RATS_ID)
        return quest is None or quest.current_step == "rejected"

    def _accept_quest(self, api: scripts.GameAPI) -> None:
        region1_quests.KillRats().start(api, allow_reset=True)

    def _reject_quest(self, api: scripts.GameAPI) -> None:
        region1_quests.KillRats().start(api, initial_step="rejected")

    def _initial_text(self, api: scripts.GameAPI) -> str:
        quest = quests_db.get_state(api, region1_quests.KILL_RATS_ID)

        if quest is None:
            return (
                "Hello, my name is Adele. I live here with my husband Cory. Are you "
                "free at the moment? I might need some help with something."
            )
        elif quest.current_step == "started":
            return (
                f"You've killed {quest.data['rats_killed']} out of "
                f"{region1_quests.KILL_RATS_TOTAL}."
            )
        elif quest.current_step == "rats_dead":
            return (
                f"You've killed all {region1_quests.KILL_RATS_TOTAL}! Thank you so "
                "much!"
            )
        elif quest.current_step == "done":
            return "Thanks for killing all those rats!"
        elif quest.current_step == "rejected":
            return "Hello again."
        else:
            raise ValueError(f"Unknown quest step {quest.current_step}")


class LouisMckayChat(conversation.GUI):
    def __init__(self):
        super().__init__(
            conversation.StaticConversation(
                title="Louis Mckay",
                text="Welcome to my shop.",
                choices=[],
            )
        )
