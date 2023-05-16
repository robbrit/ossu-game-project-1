import dataclasses
import functools
from typing import (
    List,
    Optional,
    Protocol,
)

from arcade import gui

from engine import scripts
from engine.gui import base

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
class StaticConversation:
    """A conversation that is always the same."""

    # The text to show in the bottom-left text area.
    text: str
    # A set of choices that the player may take from this conversation.
    choices: List[Choice]

    # The title to show in the top. If it's not set, falls back to the initial
    # conversation's title.
    title: Optional[str] = None


class Conversation(Protocol):
    """A conversation allows the player to interact with NPCs in the world.

    Conversations are implemented as a directed graph data structure, with the edges
    representing choices between conversations.
    """

    @property
    def text(self) -> str:
        """Gets the text to display for this conversation."""

    @property
    def choices(self) -> List[Choice]:
        """Gets a set of choices that can be made for this conversation."""

    @property
    def title(self) -> Optional[str]:
        """Gets the title to display at the top of the conversation GUI."""


class GUI(base.GUI):
    """A GUI that navigates a conversation in the game."""

    root: Conversation
    current: Conversation

    def __init__(self, root_conversation: Conversation):
        super().__init__()
        self.root = root_conversation
        self.current = self.root
        self.api = None
        self.manager = None

    def _choice_picked(self, choice: Choice, _event: gui.UIOnClickEvent):
        assert self.api is not None

        if choice.link is not None:
            self.current = choice.link

        if choice.action is not None:
            choice.action(self.api)

        self._reset_widgets()

    def _resume_game(self, event: gui.UIOnClickEvent) -> None:
        # pylint: disable=unused-argument
        assert self.api is not None
        self.api.start_game()

    def _reset_widgets(self) -> None:
        assert self.manager is not None

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
            button = gui.UIFlatButton(
                x=CHOICES_OFFSET,
                y=(
                    (len(self.current.choices) - i) * CHOICE_HEIGHT
                    + CONVERSATION_PADDING
                ),
                height=CHOICE_HEIGHT,
                text=choice.text,
            )
            button.set_handler(
                "on_click",
                functools.partial(self._choice_picked, choice),
            )
            self.manager.add(button, index=0)

        exit_button = gui.UIFlatButton(
            x=CHOICES_OFFSET,
            y=CONVERSATION_PADDING,
            height=CHOICE_HEIGHT,
            text="Bye!",
        )
        exit_button.on_click = self._resume_game  # type: ignore
        self.manager.add(exit_button, index=0)

        title = self.current.title or self.root.title
        if title is not None:
            self.manager.add(
                gui.UILabel(
                    x=CONVERSATION_PADDING,
                    y=SCREEN_HEIGHT - CONVERSATION_PADDING,
                    text=title,
                    bold=True,
                ),
                index=0,
            )
