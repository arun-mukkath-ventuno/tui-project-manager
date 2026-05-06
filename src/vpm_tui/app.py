"""Main TUI application."""

from textual.app import App

from vpm_tui.tui.screens.dashboard import DashboardScreen


class VpmTuiApp(App):
    """Main Textual application for vpm_tui."""

    TITLE = "TUI Project Manager"
    CSS_PATH = None
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())


