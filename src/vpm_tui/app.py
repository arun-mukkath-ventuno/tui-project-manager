"""Main TUI application."""

from pathlib import Path

from textual.app import App

from vpm_tui.tui.screens.dashboard import DashboardScreen


class VpmTuiApp(App):
    """Main Textual application for vpm_tui."""

    TITLE = "TUI Project Manager"
    CSS_PATH = Path(__file__).with_name("tui").joinpath("theme.tcss")
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())
