from textual import events
from textual.app import App, ComposeResult
from textual.keys import Keys
from textual.widgets import Static

from .widgets.ChatBox import ChatBox


# Constants
CONTENT_VIEW_LABEL = "Content View"
ROSTER_VIEW_LABEL = "Roster"

# Element IDs
CONTENT_VIEW_ID = "content-view"
ROSTER_VIEW_ID = "roster-view"

# CSS Classes
CSS_BOX = "box"


class BaseApp(App):

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Static(CONTENT_VIEW_LABEL, classes=CSS_BOX, id=CONTENT_VIEW_ID)
        yield ChatBox()
        yield Static(ROSTER_VIEW_LABEL, classes=CSS_BOX, id=ROSTER_VIEW_ID)

    def on_key(self, event: events.Key) -> None:
        if event.key == Keys.Enter:
            self.query_one(ChatBox).focus()


if __name__ == "__main__":
    app = BaseApp()
    app.run()
