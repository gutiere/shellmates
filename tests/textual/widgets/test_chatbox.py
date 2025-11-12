"""Tests for ChatBox widget"""

import pytest
from textual.app import App
from textual.pilot import Pilot

from shellmates.textual.widgets.ChatBox import ChatBox


class ChatBoxTestApp(App):
    """Test app for ChatBox widget"""

    def compose(self):
        yield ChatBox()


@pytest.fixture
async def chatbox_pilot():
    """Fixture that provides a pilot for testing ChatBox"""
    app = ChatBoxTestApp()
    async with app.run_test() as pilot:
        yield pilot


@pytest.mark.asyncio
async def test_chatbox_mounts_successfully(chatbox_pilot: Pilot):
    """Test that ChatBox mounts with required components"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    assert chatbox is not None
    assert chatbox.chat_input == ""
    assert len(chatbox.player_chat) == 0


@pytest.mark.asyncio
async def test_chatbox_has_chat_view(chatbox_pilot: Pilot):
    """Test that ChatBox has a chat view container"""
    # Query for the chat view by ID
    chat_view = chatbox_pilot.app.query_one("#chat-view")
    assert chat_view is not None


@pytest.mark.asyncio
async def test_chatbox_has_input_prompt(chatbox_pilot: Pilot):
    """Test that ChatBox has an input prompt"""
    input_prompt = chatbox_pilot.app.query_one("#input-prompt")
    assert input_prompt is not None
    assert "> " in str(input_prompt.render())


@pytest.mark.asyncio
async def test_chatbox_typing_updates_input(chatbox_pilot: Pilot):
    """Test that typing updates the chat input"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Simulate typing
    await chatbox_pilot.press("h", "e", "l", "l", "o")

    assert chatbox.chat_input == "hello"


@pytest.mark.asyncio
async def test_chatbox_backspace_removes_character(chatbox_pilot: Pilot):
    """Test that backspace removes characters"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Type some text
    await chatbox_pilot.press("h", "e", "l", "l", "o")
    assert chatbox.chat_input == "hello"

    # Press backspace
    await chatbox_pilot.press("backspace")
    assert chatbox.chat_input == "hell"

    # Press backspace again
    await chatbox_pilot.press("backspace")
    assert chatbox.chat_input == "hel"


@pytest.mark.asyncio
async def test_chatbox_enter_sends_message(chatbox_pilot: Pilot):
    """Test that pressing enter sends a message"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Type a message
    await chatbox_pilot.press("h", "i")
    assert chatbox.chat_input == "hi"

    # Press enter to send
    await chatbox_pilot.press("enter")

    # Input should be cleared
    assert chatbox.chat_input == ""

    # Message should be added to chat history
    assert len(chatbox.player_chat) == 1
    assert "hi" in chatbox.player_chat[0]["message"]


@pytest.mark.asyncio
async def test_chatbox_empty_message_not_sent(chatbox_pilot: Pilot):
    """Test that empty messages are not sent"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Press enter without typing anything
    await chatbox_pilot.press("enter")

    # No message should be added
    assert len(chatbox.player_chat) == 0

    # Try with just spaces
    await chatbox_pilot.press("space", "space", "enter")

    # Still no message should be added
    assert len(chatbox.player_chat) == 0


@pytest.mark.asyncio
async def test_chatbox_multiple_messages(chatbox_pilot: Pilot):
    """Test sending multiple messages"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Send first message
    await chatbox_pilot.press("f", "i", "r", "s", "t", "enter")
    assert len(chatbox.player_chat) == 1

    # Send second message
    await chatbox_pilot.press("s", "e", "c", "o", "n", "d", "enter")
    assert len(chatbox.player_chat) == 2

    # Check messages
    assert "first" in chatbox.player_chat[0]["message"]
    assert "second" in chatbox.player_chat[1]["message"]


@pytest.mark.asyncio
async def test_chatbox_player_name_in_message(chatbox_pilot: Pilot):
    """Test that player name is included in messages"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Send a message
    await chatbox_pilot.press("t", "e", "s", "t", "enter")

    # Check that player name is in the message
    assert chatbox.player_name in chatbox.player_chat[0]["message"]
    assert chatbox.player_chat[0]["user"] == chatbox.player_name


@pytest.mark.asyncio
async def test_chatbox_message_formatting(chatbox_pilot: Pilot):
    """Test that messages are formatted with timestamp"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Send a message
    await chatbox_pilot.press("t", "e", "s", "t", "enter")

    message = chatbox.player_chat[0]["message"]

    # Check for timestamp format [HH:MM:SS]
    assert message.startswith("[")
    assert "]" in message
    assert ":" in message
    assert "test" in message


@pytest.mark.asyncio
async def test_chatbox_user_color_class_system(chatbox_pilot: Pilot):
    """Test that system user gets correct color class"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    color_class = chatbox._get_user_color_class("System")
    assert color_class == "color-system"


@pytest.mark.asyncio
async def test_chatbox_user_color_class_self(chatbox_pilot: Pilot):
    """Test that current player gets self color class"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    color_class = chatbox._get_user_color_class(chatbox.player_name)
    assert color_class == "color-self"


@pytest.mark.asyncio
async def test_chatbox_user_color_class_other_players(chatbox_pilot: Pilot):
    """Test that other players get consistent color classes"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Same player should always get same color
    color1 = chatbox._get_user_color_class("Alice")
    color2 = chatbox._get_user_color_class("Alice")
    assert color1 == color2

    # Color should be one of the player colors
    assert color1.startswith("color-player")


@pytest.mark.asyncio
async def test_chatbox_user_color_class_none(chatbox_pilot: Pilot):
    """Test that None user gets default color"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    color_class = chatbox._get_user_color_class(None)
    assert color_class == "color-default"


@pytest.mark.asyncio
async def test_chatbox_input_prompt_updates(chatbox_pilot: Pilot):
    """Test that input prompt updates as user types"""
    input_prompt = chatbox_pilot.app.query_one("#input-prompt")

    # Initially should show empty input
    assert "> " in str(input_prompt.render())

    # Type some text
    await chatbox_pilot.press("h", "i")
    await chatbox_pilot.pause()

    # Prompt should show the typed text
    assert "> hi" in str(input_prompt.render())
