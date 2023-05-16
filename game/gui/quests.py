import functools
from typing import (
    List,
    Optional,
    Tuple,
)

from arcade import (
    csscolor,
    gui,
)

from engine import (
    core,
    scripts,
)
from engine.gui import base
from game.quests import (
    base as quests,
    db as quest_db,
)

GUI_PADDING = 5


class GUI(base.GUI):
    """A GUI that shows all the quests for the player."""

    _quest_title: Optional[gui.UILabel]
    _quest_description: Optional[gui.UITextArea]

    def __init__(self):
        super().__init__()
        self._quest_title = None
        self._quest_description = None

    def _select_quest(
        self,
        quest: quests.Quest,
        quest_state: quests.QuestState,
        _event: gui.UIEvent,
    ) -> None:
        assert self._quest_title is not None
        assert self._quest_description is not None

        self._quest_title.text = quest.title
        self._quest_title.fit_content()
        self._quest_description.text = quest.steps[quest_state.current_step].description

    def _reset_widgets(self) -> None:
        assert self.api is not None
        assert self.manager is not None

        self.manager.clear()
        # Dirty hack to get the UI manager to reset correctly.
        self.manager.children[0] = []

        quest_states: List[Tuple[quests.Quest, quests.QuestState]] = [
            (quest_db.get(quest_id), quest_state)
            for quest_id, quest_state in self.api.player_data["quests"].items()
        ]

        self._quest_title = gui.UILabel(size_hint=(1.0, 0.1), text="")
        self._quest_description = gui.UITextArea(size_hint=(1.0, 0.9), text="")

        quest_details_pane = gui.UIBoxLayout(
            vertical=True,
            size_hint=(0.5, 1.0),
            children=(self._quest_title, self._quest_description),
            space_between=GUI_PADDING,
        )
        resume_button = gui.UIFlatButton(text="Resume")

        @resume_button.event("on_click")
        def _on_resume_button(_event: gui.UIEvent) -> None:
            assert self.api is not None
            self.api.start_game()

        quest_buttons: List[gui.UIWidget] = []

        for quest, quest_state in quest_states:
            button = gui.UIFlatButton(
                size_hint=(1.0, None),
                height=30,
                text=quest.title,
            )
            button.set_handler(
                "on_click",
                functools.partial(
                    self._select_quest,
                    quest=quest,
                    quest_state=quest_state,
                ),
            )
            quest_buttons.append(button)

        if not quest_buttons:
            quest_buttons.append(gui.UILabel(italic=True, text="No quests yet"))

        main_layout = gui.UIBoxLayout(
            vertical=True,
            space_between=GUI_PADDING,
            children=(
                gui.UIBoxLayout(
                    vertical=False,
                    size_hint=(1.0, 0.8),
                    space_between=GUI_PADDING,
                    children=(
                        gui.UIBoxLayout(
                            vertical=True,
                            children=[
                                gui.UILabel(text="Quests"),
                            ]
                            + quest_buttons,
                            space_between=GUI_PADDING,
                            size_hint=(0.5, 1.0),
                        )
                        .with_space_around(
                            GUI_PADDING, GUI_PADDING, GUI_PADDING, GUI_PADDING
                        )
                        .with_border(color=csscolor.WHITE),
                        quest_details_pane.with_space_around(
                            GUI_PADDING, GUI_PADDING, GUI_PADDING, GUI_PADDING
                        ).with_border(color=csscolor.WHITE),
                    ),
                ),
                gui.UIBoxLayout(size_hint=(1.0, 0.2), children=(resume_button,)),
            ),
        )

        anchor = gui.UIAnchorWidget(
            width=core.SCREEN_WIDTH,
            height=core.SCREEN_HEIGHT,
            child=gui.UIWrapper(child=main_layout, size_hint=(1.0, 1.0)),
        )

        self.manager.add(anchor, index=0)


def show_quests_gui(api: scripts.GameAPI) -> None:
    """Shows the quests GUI."""
    api.show_gui(GUI())
