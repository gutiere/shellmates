[![PyPI version](https://badge.fury.io/py/shellmates.svg?)](https://badge.fury.io/py/shellmates)
![OS support](https://img.shields.io/badge/OS-macOS%20Linux-red)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

![](resources/shellmates.png)

# shellmates

A terminal based gaming hub.

> 🎮 Play classic games right in your terminal - no GUI needed!

## ✨ Features

-   🕹️ Collection of classic terminal-based games
-   🎯 Simple and intuitive command-line interface
-   🏆 Score tracking and leaderboards (coming soon)
-   👥 Multiplayer support (coming soon)
-   🎨 Customizable themes and color schemes (coming soon)
-   📊 Game statistics and achievements (coming soon)
-   💾 Save/load game progress (coming soon)
-   🔌 Plugin system for adding custom games (coming soon)

## 🎮 Available Games

-   **Snake** - Classic snake game with modern controls (coming soon)
-   **Tetris** - Block-stacking puzzle game (coming soon)
-   **Pong** - Two-player paddle game (coming soon)
-   **Minesweeper** - Logic-based mine detection game (coming soon)
-   **2048** - Number sliding puzzle (coming soon)
-   **Tic-Tac-Toe** - Classic strategy game (coming soon)
-   _More games coming soon!_

## 🚀 Quick Start

### Installation

#### Using pip

```bash
pip install shellmates
```

#### Using poetry

```bash
poetry add shellmates
```

#### Using uv

```bash
uv pip install shellmates
```

#### From source

```bash
# Clone the repository
git clone https://github.com/gutiere/shellmates.git
cd shellmates

# Using pip
pip install -e .

# Using poetry
poetry install

# Using uv
uv pip install -e .
```

### Usage

```bash
# Launch the game hub
shellmates

# Play a specific game directly
shellmates play snake

# Get help
shellmates --help
```

## 📋 Requirements

-   Python 3.10 or higher
-   Terminal with 256-color support
-   macOS or Linux (Windows support coming soon)

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/gutiere/shellmates.git
cd shellmates

# Create virtual environment with uv
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies with uv
uv pip install -e ".[dev]"

# Run tests
pytest
```

### Project Structure

```
shellmates/
├── src/
│   └── shellmates/
│       ├── __init__.py
│       ├── main.py             # Main entry point
│       └── textual/            # Textual TUI components
│           ├── app.py          # BaseApp - main application
│           ├── app.tcss        # TUI styling
│           └── widgets/        # Custom widgets
│               └── ChatBox.py  # Chat widget
├── tests/                      # Test suite (mirrors src structure)
│   ├── __init__.py
│   └── textual/
│       ├── __init__.py
│       ├── test_app.py         # BaseApp tests
│       └── widgets/
│           ├── __init__.py
│           └── test_chatbox.py # ChatBox tests
├── resources/                  # Assets and resources
├── scripts/                    # Utility scripts
│   └── deploy.sh
├── pyproject.toml             # Project configuration
├── setup.py                   # Setup configuration
├── TESTING.md                 # Testing documentation
├── CONTRIBUTING.md
└── README.md
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-game`)
3. Commit your changes (`git commit -m 'Add amazing new game'`)
4. Push to the branch (`git push origin feature/amazing-game`)
5. Open a Pull Request

### Adding a New Game

Want to add a new game to shellmates? Check out our [Game Development Guide](docs/GAME_DEVELOPMENT.md) for instructions on creating custom games.

## 📖 Documentation

Full documentation is available at [https://shellmates.readthedocs.io](https://shellmates.readthedocs.io)

-   [User Guide](docs/user-guide.md)
-   [API Reference](docs/api-reference.md)
-   [Game Development Guide](docs/game-development.md)
-   [Configuration](docs/configuration.md)
-   [FAQ](docs/faq.md)

## 🐛 Bug Reports & Feature Requests

Found a bug or have an idea for a new feature? Please open an issue on our [GitHub Issues](https://github.com/gutiere/shellmates/issues) page.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each release.

## 🏆 Credits

Created and maintained by

-   [Elijah Gutierrez](https://github.com/gutiere)
-   [Caleb Ice](https://github.com/calebice)
-   [Jackson Kelley](https://github.com/jkelley253)

<!-- Special thanks to all our [contributors](https://github.com/gutiere/shellmates/graphs/contributors)! -->

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Show Your Support

If you like this project, please consider:

-   ⭐ Starring the repository
-   🐦 Sharing it on social media

## 📧 Contact

-   GitHub: [@gutiere](https://github.com/gutiere)
-   Email: [edgardogutierrezjr@gmail.com](mailto:edgardogutierrezjr@gmail.com)

---

Made with ❤️ by the shellmates community
