# Shellmates Testing Guide

This guide explains how to run and write tests for the Shellmates project.

## Setup

First, install the development dependencies using uv:

```bash
uv pip install -e ".[dev]"
```

Or sync all dependencies:

```bash
uv sync
```

This installs:

-   `pytest` - Testing framework
-   `pytest-asyncio` - For testing async code

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run specific test file:

```bash
pytest tests/textual/widgets/test_chatbox.py
```

Run specific test:

```bash
pytest tests/textual/widgets/test_chatbox.py::test_chatbox_typing_updates_input
```

Run with coverage:

```bash
pytest --cov=shellmates --cov-report=html
```

## Writing Tests for Textual Apps

Textual provides the `run_test()` method and `Pilot` API for testing.

### Basic Test Structure

```python
import pytest
from textual.app import App
from textual.pilot import Pilot

class MyTestApp(App):
    def compose(self):
        yield MyWidget()

@pytest.fixture
async def app_pilot():
    app = MyTestApp()
    async with app.run_test() as pilot:
        yield pilot

@pytest.mark.asyncio
async def test_something(app_pilot: Pilot):
    widget = app_pilot.app.query_one(MyWidget)
    assert widget is not None
```

### Key Testing Methods

**Simulating Key Presses:**

```python
await pilot.press("h", "e", "l", "l", "o")  # Type letters
await pilot.press("enter")                   # Press enter
await pilot.press("backspace")               # Press backspace
```

**Querying Widgets:**

```python
widget = pilot.app.query_one(ChatBox)              # Get widget by type
element = pilot.app.query_one("#my-id")            # Get by ID
elements = pilot.app.query(".my-class")            # Get by class
```

**Accessing Widget Content:**

```python
static_widget = pilot.app.query_one("#my-static")
content = str(static_widget.render())              # Get rendered content
assert "Expected text" in content
```

**Waiting and Pausing:**

```python
await pilot.pause()      # Wait for app to process
await pilot.wait_for_scheduled_animations()  # Wait for animations
```

**Clicking:**

```python
await pilot.click("#my-button")
```

## Test Structure

Tests are organized to mirror the source structure:

```
tests/
├── __init__.py
└── textual/
    ├── __init__.py
    ├── test_app.py          # Tests for BaseApp
    └── widgets/
        ├── __init__.py
        └── test_chatbox.py  # Tests for ChatBox widget
```

## Test Coverage

Current test coverage (23 tests, all passing):

### ChatBox Widget (15 tests)

-   ✅ Widget mounting and initialization
-   ✅ Chat view and input prompt components
-   ✅ User input handling (typing, backspace)
-   ✅ Message sending and validation
-   ✅ Empty message prevention
-   ✅ Multiple message handling
-   ✅ Message formatting with timestamps
-   ✅ Color class assignment (system, self, other players, none)
-   ✅ Input prompt updates

### BaseApp (8 tests)

-   ✅ App mounting with all components
-   ✅ Content view presence and rendering
-   ✅ Roster view presence and rendering
-   ✅ ChatBox integration
-   ✅ Input handling through app
-   ✅ Message sending through app
-   ✅ Layout structure validation
-   ✅ CSS loading

## Best Practices

1. **Use fixtures** for common setup (app pilots, test data)
2. **Mark async tests** with `@pytest.mark.asyncio`
3. **Test user interactions** through the Pilot API, not directly
4. **Assert on widget state** after simulating actions
5. **Test edge cases** (empty inputs, special characters, etc.)
6. **Keep tests isolated** - each test should be independent
7. **Use descriptive names** - test names should explain what they verify

## Example: Testing a Widget Method

```python
@pytest.mark.asyncio
async def test_chatbox_color_assignment(chatbox_pilot: Pilot):
    """Test that users get consistent color classes"""
    chatbox = chatbox_pilot.app.query_one(ChatBox)

    # Test method directly
    color1 = chatbox._get_user_color_class("Alice")
    color2 = chatbox._get_user_color_class("Alice")

    # Same user should get same color
    assert color1 == color2
```

## Example: Testing User Interaction

```python
@pytest.mark.asyncio
async def test_send_message_flow(app_pilot: Pilot):
    """Test complete message sending flow"""
    chatbox = app_pilot.app.query_one(ChatBox)

    # Type a message
    await app_pilot.press("h", "e", "l", "l", "o")
    assert chatbox.chat_input == "hello"

    # Send it
    await app_pilot.press("enter")

    # Verify results
    assert chatbox.chat_input == ""
    assert len(chatbox.player_chat) == 1
    assert "hello" in chatbox.player_chat[0]["message"]
```

## Troubleshooting

**Command not found: pytest:** Make sure you've installed the dev dependencies:

```bash
uv pip install -e ".[dev]"
# or
uv sync
```

**Import errors:** Ensure the package is installed in development mode and you're using the correct Python environment.

**Async warnings:** Ensure `pytest-asyncio` is installed and tests are marked with `@pytest.mark.asyncio`. The `asyncio_mode = "auto"` setting in `pyproject.toml` should handle this automatically.

**Widget not found:** Use `await pilot.pause()` before querying to ensure widgets are mounted.

**AttributeError on Static widgets:** Use `str(widget.render())` instead of `widget.renderable` to access widget content.

## Additional Resources

-   [Textual Testing Documentation](https://textual.textualize.io/guide/testing/)
-   [Pytest Documentation](https://docs.pytest.org/)
-   [Pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
