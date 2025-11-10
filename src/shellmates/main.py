import threading

from shellmates.textual.app import BaseApp


def run_core_server():
    """Run the FastAPI server in a background thread"""
    pass


def main():

    # Start Core Server
    api_thread = threading.Thread(target=run_core_server, daemon=True)
    api_thread.start()

    # Run Textual app in the main thread (so it controls the terminal)
    app = BaseApp()
    app.run()


if __name__ == "__main__":
    main()
