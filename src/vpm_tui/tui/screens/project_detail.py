"""Project detail screen."""

import asyncio

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from vpm_tui.ai.summarizer import ProjectSummarizer
from vpm_tui.config import settings
from vpm_tui.db.repo import ProjectRepository
from vpm_tui.db.session import SessionLocal
from vpm_tui.tui.screens.task_detail import TaskDetailScreen
from vpm_tui.tui.widgets.summary_panel import SummaryPanel


class ProjectDetailScreen(Screen):
    """Project detail drilldown screen with AI summary panel."""

    BINDINGS = [
        ("escape", "pop_screen", "Back"),
        ("q", "pop_screen", "Back"),
        ("s", "summarize", "Summarize"),
    ]

    def __init__(self, project_slug: str) -> None:
        self.project_slug = project_slug
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("", id="project-header")
            yield SummaryPanel(id="summary-panel")
            table = DataTable(id="tasks-table")
            table.cursor_type = "row"
            yield table
            yield Static("", id="project-footer")
        yield Footer()

    def on_mount(self) -> None:
        self._load_project()

    async def action_summarize(self) -> None:
        """Generate AI summary in background thread."""
        panel = self.query_one("#summary-panel", SummaryPanel)

        if not settings.openai_api_key:
            panel.show_error("OPENAI_API_KEY not set in .env")
            return

        panel.show_loading()

        summarizer = ProjectSummarizer()
        try:
            summary = await asyncio.to_thread(
                summarizer.summarize, self.project_slug
            )
        except Exception as e:
            panel.show_error(str(e))
            return

        panel.show_summary(summary)

    def _load_project(self) -> None:
        header = self.query_one("#project-header", Static)
        table = self.query_one("#tasks-table", DataTable)
        footer = self.query_one("#project-footer", Static)

        table.clear(columns=True)
        table.add_columns("Phase", "Task", "Status", "Owner")

        with SessionLocal() as session:
            repo = ProjectRepository(session)
            project = repo.get_with_details(self.project_slug)
            if not project:
                header.update(f"Project '{self.project_slug}' not found")
                return

            counts: dict[str, int] = {}
            total = 0
            for phase in project.phases:
                for task in phase.tasks:
                    counts[task.status] = counts.get(task.status, 0) + 1
                    total += 1
                    table.add_row(
                        phase.name,
                        task.title,
                        task.status,
                        task.owner or "-",
                        key=task.id,
                    )

            header.update(
                f"[b]{project.name}[/b] — {total} tasks  "
                f"open={counts.get('open', 0)} wip={counts.get('wip', 0)} "
                f"done={counts.get('dev-complete', 0)}"
            )
            footer.update(f"Source: {project.source_path}")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        task_id = event.row_key.value
        self.app.push_screen(TaskDetailScreen(task_id))
