"""This file contains all the quests for region 1."""

from typing import (
    Any,
    Callable,
    cast,
    Dict,
)

from engine import scripts
from game.quests import (
    base,
    db,
    quest_script,
)
from game.scripts import events

KILL_RATS_ID = "region1.kill_rats"
KILL_RATS_TOTAL = 3
KILL_RATS_QUEST = base.Quest(
    name=KILL_RATS_ID,
    title="Kill the Rats",
    steps={
        "started": base.QuestStep(
            description=(
                f"Adele Cotton has asked me to go kill {KILL_RATS_TOTAL} rats. I "
                "should go to the forest to the west and kill some."
            ),
        ),
        "rats_dead": base.QuestStep(
            description=(
                f"I've killed {KILL_RATS_TOTAL} rats. I should go back to Adele and "
                "report to her."
            ),
        ),
        "done": base.QuestStep(
            description="Adele was very pleased with me.",
        ),
        "rejected": base.QuestStep(
            description="I declined to go kill some rats.",
        ),
    },
    initial_step="started",
    initial_data=cast(
        Callable[[scripts.GameAPI], Dict[str, Any]],
        lambda _api: {"rats_killed": 0},
    ),
)


def register():
    """Registers all region1 quests."""
    db.register(KILL_RATS_QUEST)


class KillRats(quest_script.QuestScript):
    """Quest to manage killing rats."""

    def __init__(self):
        super().__init__(KILL_RATS_QUEST)

    def set_api(self, api: scripts.GameAPI):
        """Sets the API for this script."""
        super().set_api(api)

        if self.quest_state != "started":
            return

        api.register_handler(events.CREATURE_KILLED, self._on_creature_killed)

    def _on_creature_killed(self, _event_type: str, data: events.CreatureKilled):
        assert self.api is not None

        if data.creature_type != "rat":
            return

        state = self.quest_state

        if state != "started":
            return

        kill_count = cast(int, state.data["rats_killed"]) + 1

        if kill_count >= KILL_RATS_TOTAL:
            self.quest_state = base.QuestState(
                current_step="rats_dead",
                data={},
                timestamp=self.api.current_time_secs,
            )
        else:
            self.quest_state = base.QuestState(
                current_step="started",
                data={"rats_killed": kill_count},
                timestamp=self.api.current_time_secs,
            )
