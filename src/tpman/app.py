"""Main TUI application."""

from textual.app import App

from tpman.tui.screens.dashboard import DashboardScreen


class TpmApp(App):
    """Main Textual application for tpman."""

    TITLE = "TUI Project Manager"
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())


