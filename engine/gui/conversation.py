import dataclasses
from typing import (
    List,
    Optional,
)

from arcade import gui

from engine import scripts

CONVERSATION_PADDING = 10
CONVERSATION_Y = 200
CONVERSATION_HEIGHT = 180
SCREEN_HEIGHT = 600
CHOICES_OFFSET = 650
CHOICE_HEIGHT = 30


@dataclasses.dataclass
class Choice:
    """A choice within a conversation. Allows the player to choose different outcomes."""

    # The text to show on the button for this choice.
    text: str
    # A conversation to link to when they make this choice.
    link: "Optional[Conversation]" = None
    # An action to take when they make this choice.
    action: Optional[scripts.GameCallable] = None


@dataclasses.dataclass
class Conversation:
    """A conversation allows the player to interact with NPCs in the world.

    Conversations are implemented as a directed graph data structure, with the edges
    leading from a conversation
    """

    # The text to show in the bottom-left text area.
    text: str
    # A set of choices that the player may take from this conversation.
    choices: List[Choice]

    # The title to show in the top. If it's not set, falls back to the initial
    # conversation's title.
    title: Optional[str] = None


class _ChoiceButton(gui.UIFlatButton):
    """Class to allow us to attach data to a UI Button."""

    index: int

    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index


class GUI:
    """A GUI that navigates a conversation in the game."""

    root: Conversation
    current: Conversation

    api: Optional[scripts.GameAPI]
    manager: Optional[gui.UIManager]

    def __init__(self, root_conversation: Conversation):
        self.root = root_conversation
        self.current = self.root
        self.api = None
        self.manager = None

    def set_api(self, api: scripts.GameAPI) -> None:
        """Sets the game API for this GUI."""
        self.api = api

    def set_manager(self, manager: gui.UIManager) -> None:
        """Sets the UI manager for this GUI."""
        self.manager = manager

        self.manager.clear()
        self._reset_widgets()

    def draw(self) -> None:
        """Renders the conversation."""

    def _choice_picked(self, event: gui.UIOnClickEvent):
        index = event.source.index
        choice = self.current.choices[index]

        if choice.link is not None:
            self.current = choice.link

        if choice.action is not None:
            choice.action(self.api)

        self._reset_widgets()

    def _resume_game(self, event: gui.UIOnClickEvent) -> None:
        self.api.start_game()

    def _reset_widgets(self) -> None:
        self.manager.clear()
        # Dirty hack to get the UI manager to reset correctly.
        self.manager.children[0] = []

        self.manager.add(
            gui.UITextArea(
                x=CONVERSATION_PADDING,
                y=CONVERSATION_Y,
                height=CONVERSATION_HEIGHT,
                text=self.current.text,
            ),
            index=0,
        )

        for i, choice in enumerate(self.current.choices):
            button = _ChoiceButton(
                index=i,
                x=CHOICES_OFFSET,
                y=(i + 1) * CHOICE_HEIGHT + CONVERSATION_PADDING,
                height=CHOICE_HEIGHT,
                text=choice.text,
            )
            button.on_click = self._choice_picked
            self.manager.add(button, index=0)

        exit_button = gui.UIFlatButton(
            x=CHOICES_OFFSET,
            y=CONVERSATION_PADDING,
            height=CHOICE_HEIGHT,
            text="Bye!",
        )
        exit_button.on_click = self._resume_game
        self.manager.add(exit_button, index=0)

        title = self.current.title or self.root.title
        if title is not None:
            # TODO(rob): Programmatically get the height of the window to figure out
            # where to put the title.
            self.manager.add(
                gui.UILabel(
                    x=CONVERSATION_PADDING,
                    y=SCREEN_HEIGHT - CONVERSATION_PADDING,
                    text=title,
                    bold=True,
                ),
                index=0,
            )
