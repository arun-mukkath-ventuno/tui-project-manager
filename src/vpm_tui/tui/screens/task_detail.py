"""Task detail screen."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from vpm_tui.db.schema import TaskRecord
from vpm_tui.db.session import SessionLocal


class TaskDetailScreen(Screen):
    """Task detail screen."""

    BINDINGS = []

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.app.pop_screen()
            event.stop()

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="app-shell"):
            with Container(classes="task-card"):
                yield Static("", id="task-info")
        yield Footer()

    def on_mount(self) -> None:
        self._load_task()

    def _load_task(self) -> None:
        info = self.query_one("#task-info", Static)

        with SessionLocal() as session:
            task = session.get(TaskRecord, self.task_id)
            if not task:
                info.update(f"Task '{self.task_id}' not found")
                return

            phase = task.phase
            project = phase.project

            lines = [
                f"[b]Task[/b]\n{task.title}",
                "",
                f"[b]Status[/b]    [dim]{task.status}[/dim]",
                f"[b]Owner[/b]     [dim]{task.owner or '-'}[/dim]",
                f"[b]Phase[/b]     [dim]{phase.name}[/dim]",
                f"[b]Project[/b]   [dim]{project.name}[/dim]",
                f"[b]Source[/b]    [dim]{task.source_file}[/dim]",
                "",
                "[dim]Press [b]q[/b] to go back[/dim]",
            ]
            info.update("\n".join(lines))
