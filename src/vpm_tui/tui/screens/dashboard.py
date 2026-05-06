"""Dashboard screen."""

import json

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header, Static

from vpm_tui.db.repo import ProjectRepository
from vpm_tui.db.session import SessionLocal


class DashboardScreen(Screen):
    """Main dashboard screen showing all projects and status counts."""

    BINDINGS = [
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("TUI Project Manager — Dashboard", id="title")
            table = DataTable(id="projects-table")
            table.cursor_type = "row"
            yield table
            yield Static("", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        self._load_projects()

    def action_refresh(self) -> None:
        from vpm_tui.config import settings
        from vpm_tui.ingest.sync import init_db, sync_directory

        if settings.projects_dir.exists():
            init_db()
            with SessionLocal() as session:
                results = sync_directory(session, settings.projects_dir)
                status = self.query_one("#status-bar", Static)
                status.update(
                    f"Synced {results['projects']} projects, {results['phases']} phases, "
                    f"{results['tasks']} tasks"
                )
        self._load_projects()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        slug = event.row_key.value
        from vpm_tui.tui.screens.project_detail import ProjectDetailScreen

        self.app.push_screen(ProjectDetailScreen(slug))

    def _load_projects(self) -> None:
        table = self.query_one("#projects-table", DataTable)
        table.clear(columns=True)
        table.add_columns(
            "Project",
            "Total",
            "Open",
            "WIP",
            "Dev Complete",
            "QA Complete",
            "In Production",
            "Last Synced",
        )

        with SessionLocal() as session:
            repo = ProjectRepository(session)
            projects = repo.get_all()
            total_tasks = 0
            for p in projects:
                counts = json.loads(p.task_counts or "{}")
                total = sum(counts.values())
                total_tasks += total
                table.add_row(
                    p.name,
                    str(total),
                    str(counts.get("open", 0)),
                    str(counts.get("wip", 0)),
                    str(counts.get("dev-complete", 0)),
                    str(counts.get("qa-complete", 0)),
                    str(counts.get("in-production", 0)),
                    str(p.last_synced_at)[:19] if p.last_synced_at else "-",
                    key=p.slug,
                )

            status = self.query_one("#status-bar", Static)
            if projects:
                status.update(
                    f"{len(projects)} projects, {total_tasks} tasks — press [b]r[/b] to refresh"
                )
            else:
                status.update(
                    "No projects found. Run [b]tpman refresh[/b] to sync from markdown sources."
                )
