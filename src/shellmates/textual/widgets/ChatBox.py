import sys
from datetime import datetime

import websockets
from textual import events, work
from textual.app import Widget, ComposeResult
from textual.containers import VerticalScroll
from textual.keys import Keys
from textual.widgets import Static

# Constants
DEFAULT_PLAYER_NAME = "Player X"
PROMPT_FORMAT = "> %s"
TIMESTAMP_FORMAT = "%H:%M:%S"

# Element IDs
CHAT_VIEW_ID = "#chat-view"
INPUT_PROMPT_ID = "#input-prompt"

# CSS Classes
CSS_CHAT_INPUT_PROMPT = "chat-input-prompt"
CSS_CHAT_MESSAGE = "chat-message"

# Color Classes
COLOR_DEFAULT = "color-default"
COLOR_SYSTEM = "color-system"
COLOR_SELF = "color-self"
COLOR_PLAYER_CLASSES = [
    "color-player1",
    "color-player2",
    "color-player3",
    "color-player4",
]

# Command Line Arguments
ARG_NAME = "--name"

# System User
SYSTEM_USER = "System"


class ChatBox(Widget):

    CSS_PATH = "../app.tcss"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.player_chat = []
        self.chat_input = ""
        self.player_name = (
            sys.argv[sys.argv.index(ARG_NAME) + 1]
            if ARG_NAME in sys.argv and sys.argv.index(ARG_NAME) + 1 < len(sys.argv)
            else DEFAULT_PLAYER_NAME
        )
        self.ws = None
        self.ws_connected = False

    def compose(self) -> ComposeResult:
        yield VerticalScroll(id=CHAT_VIEW_ID.lstrip("#"))
        yield Static(
            PROMPT_FORMAT % self.chat_input,
            id=INPUT_PROMPT_ID.lstrip("#"),
            classes=CSS_CHAT_INPUT_PROMPT,
        )

    def on_mount(self) -> None:
        # Scroll to bottom after adding new message
        chat_view = self.query_one(CHAT_VIEW_ID, VerticalScroll)
        chat_view.scroll_end(animate=False)

        # Connect to WebSocket server
        if websockets:
            self._connect_websocket()

    def on_key(self, event: events.Key) -> None:
        if event.key == Keys.Backspace:
            self.chat_input = self.chat_input[:-1]
        elif event.key == Keys.Enter:

            # Disable sending empty messages
            if not self.chat_input.strip():
                return

            # Send message via WebSocket if connected
            if self.ws_connected and self.chat_input:
                self.send_message(self.chat_input)

            # Fallback to local display
            else:
                self._add_message(self.chat_input)
            self.chat_input = ""
        else:
            try:
                self.chat_input += event.character
            except Exception:
                pass

        # Update the input prompt display
        self._update_input_prompt()

    def _format_message_for_transcript(self, message: str) -> str:
        now = datetime.now()
        timestamp = now.strftime(TIMESTAMP_FORMAT)
        timestamped_message = f"[{timestamp}] {self.player_name}: {message}"
        return timestamped_message

    def _add_message(self, message: str) -> None:
        """Add a message to the chat"""

        transcript_message = self._format_message_for_transcript(message)

        self.player_chat.append(
            {"user": self.player_name, "message": transcript_message}
        )

        color_class = self._get_user_color_class(self.player_name)
        message_widget = Static(
            transcript_message, classes=f"{CSS_CHAT_MESSAGE} {color_class}"
        )
        chat_view = self.query_one(CHAT_VIEW_ID, VerticalScroll)
        chat_view.mount(message_widget)
        chat_view.scroll_end(animate=False)

    def _update_input_prompt(self) -> None:
        """Update the input prompt and scroll chat view to bottom"""

        # Update input prompt
        prompt = self.query_one(INPUT_PROMPT_ID, Static)
        prompt.update(PROMPT_FORMAT % self.chat_input)

        # Scroll chat view to bottom
        chat_view = self.query_one(CHAT_VIEW_ID, VerticalScroll)
        chat_view.scroll_end(animate=False)

    def _get_user_color_class(self, user: str) -> str:
        """Get a color class for a user"""
        if user is None:
            return COLOR_DEFAULT
        elif user == SYSTEM_USER:
            return COLOR_SYSTEM
        elif user == self.player_name:
            return COLOR_SELF
        else:
            # Hash username to consistent color
            color_index = hash(user) % len(COLOR_PLAYER_CLASSES)
            return COLOR_PLAYER_CLASSES[color_index]

    @work(exclusive=True)
    async def _connect_websocket(self) -> None:
        """Connect to the WebSocket server with retry logic"""
        pass
