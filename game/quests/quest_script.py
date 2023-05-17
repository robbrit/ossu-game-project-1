from typing import (
    cast,
    Dict,
    Optional,
)

from engine import scripts
from game.quests import (
    base,
    db,
)


class QuestScript(scripts.SavesAPI, scripts.Script):
    """Wraps a bunch of functionality around quests."""

    _quest: base.Quest

    def __init__(self, quest: base.Quest):
        super().__init__()
        self._quest = quest

    def start(
        self,
        api: scripts.GameAPI,
        initial_step: Optional[str] = None,
        allow_reset: bool = False,
    ) -> None:
        """Starts the quest."""

        quests = cast(Dict[str, base.QuestState], api.player_data["quests"])

        if self._quest.name in quests and not allow_reset:
            return

        quests[self._quest.name] = base.QuestState(
            current_step=initial_step or self._quest.initial_step,
            data=self._quest.initial_data(api),
            timestamp=api.current_time_secs,
        )

    @property
    def quest_state(self) -> base.QuestState:
        """Gets the quest state for this quest."""
        assert self.api is not None
        state = db.get_state(self.api, self._quest.name)
        assert state is not None, "Quest state should be set already!"
        return state

    @quest_state.setter
    def quest_state(self, value: base.QuestState) -> None:
        """Sets the quest state for this quest."""
        assert self.api is not None
        db.set_state(self.api, self._quest.name, value)
