"""Task detail screen."""

from textual.app import ComposeResult
from textual.containers import Vertical
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
        with Vertical():
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
                f"[b]Task:[/b]      {task.title}",
                f"[b]Status:[/b]    {task.status}",
                f"[b]Owner:[/b]     {task.owner or '-'}",
                f"[b]Phase:[/b]     {phase.name}",
                f"[b]Project:[/b]   {project.name}",
                f"[b]Source:[/b]    {task.source_file}",
                "",
                "[dim]Press [b]q[/b] to go back[/dim]",
            ]
            info.update("\n".join(lines))
