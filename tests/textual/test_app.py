"""Tests for BaseApp application"""

import pytest
from textual.pilot import Pilot

from shellmates.textual.app import BaseApp
from shellmates.textual.widgets.ChatBox import ChatBox


@pytest.fixture
async def app_pilot():
    """Fixture that provides a pilot for testing BaseApp"""
    app = BaseApp()
    async with app.run_test() as pilot:
        yield pilot


@pytest.mark.asyncio
async def test_app_mounts_successfully(app_pilot: Pilot):
    """Test that the app mounts with all required components"""
    # Check that all main components are present
    content_view = app_pilot.app.query_one("#content-view")
    chatbox = app_pilot.app.query_one(ChatBox)
    roster_view = app_pilot.app.query_one("#roster-view")

    assert content_view is not None
    assert chatbox is not None
    assert roster_view is not None


@pytest.mark.asyncio
async def test_app_has_content_view(app_pilot: Pilot):
    """Test that app has a content view"""
    content_view = app_pilot.app.query_one("#content-view")
    assert content_view is not None
    assert "Content View" in str(content_view.render())


@pytest.mark.asyncio
async def test_app_has_roster_view(app_pilot: Pilot):
    """Test that app has a roster view"""
    roster_view = app_pilot.app.query_one("#roster-view")
    assert roster_view is not None
    assert "Roster" in str(roster_view.render())


@pytest.mark.asyncio
async def test_app_has_chatbox(app_pilot: Pilot):
    """Test that app includes ChatBox widget"""
    chatbox = app_pilot.app.query_one(ChatBox)
    assert chatbox is not None
    assert isinstance(chatbox, ChatBox)


@pytest.mark.asyncio
async def test_app_chatbox_receives_input(app_pilot: Pilot):
    """Test that ChatBox in the app can receive input"""
    chatbox = app_pilot.app.query_one(ChatBox)

    # Type into the chatbox
    await app_pilot.press("h", "e", "l", "l", "o")

    # Verify input was received
    assert chatbox.chat_input == "hello"


@pytest.mark.asyncio
async def test_app_chatbox_sends_messages(app_pilot: Pilot):
    """Test that messages can be sent through the app"""
    chatbox = app_pilot.app.query_one(ChatBox)

    # Send a message
    await app_pilot.press("t", "e", "s", "t", "enter")

    # Verify message was added
    assert len(chatbox.player_chat) == 1
    assert "test" in chatbox.player_chat[0]["message"]


@pytest.mark.asyncio
async def test_app_layout_structure(app_pilot: Pilot):
    """Test that app has the expected layout structure"""
    # Get all widgets with the 'box' class
    boxes = app_pilot.app.query(".box")

    # Should have content-view and roster-view with 'box' class
    assert len(boxes) >= 2

    # Verify IDs
    ids = [widget.id for widget in boxes]
    assert "content-view" in ids
    assert "roster-view" in ids


@pytest.mark.asyncio
async def test_app_css_loaded(app_pilot: Pilot):
    """Test that CSS is loaded for the app"""
    # The app should have CSS_PATH set
    assert hasattr(app_pilot.app, "CSS_PATH")
    assert app_pilot.app.CSS_PATH == "app.tcss"
