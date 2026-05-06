"""MCP tools exposed to agents."""

import json

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from tpman.config import settings
from tpman.db.repo import ProjectRepository
from tpman.db.schema import PhaseRecord, ProjectRecord, TaskRecord
from tpman.db.session import SessionLocal
from tpman.ingest.sync import init_db, sync_directory


def register_tools(mcp):
    @mcp.tool()
    def list_projects() -> str:
        """List all projects with task counts."""
        with SessionLocal() as session:
            repo = ProjectRepository(session)
            projects = repo.get_all()
            result = []
            for p in projects:
                counts = json.loads(p.task_counts or "{}")
                result.append(
                    {
                        "name": p.name,
                        "slug": p.slug,
                        "total_tasks": sum(counts.values()),
                        "counts": counts,
                    }
                )
            return json.dumps(result, indent=2)

    @mcp.tool()
    def get_project_detail(slug: str) -> str:
        """Get detailed information about a project by slug."""
        with SessionLocal() as session:
            repo = ProjectRepository(session)
            project = repo.get_with_details(slug)
            if not project:
                return json.dumps({"error": f"Project '{slug}' not found"})

            counts = json.loads(project.task_counts or "{}")
            phases = []
            for phase in project.phases:
                tasks = [
                    {"title": t.title, "status": t.status, "owner": t.owner}
                    for t in phase.tasks
                ]
                phases.append(
                    {"name": phase.name, "order": phase.order, "tasks": tasks}
                )

            return json.dumps(
                {
                    "name": project.name,
                    "slug": project.slug,
                    "source_path": project.source_path,
                    "total_tasks": sum(counts.values()),
                    "counts": counts,
                    "phases": phases,
                },
                indent=2,
            )

    @mcp.tool()
    def list_tasks(project_slug: str | None = None) -> str:
        """List tasks, optionally filtered by project slug."""
        with SessionLocal() as session:
            stmt = select(TaskRecord).options(selectinload(TaskRecord.phase))
            if project_slug:
                stmt = (
                    stmt.join(
                        PhaseRecord, TaskRecord.phase_id == PhaseRecord.id
                    )
                    .join(
                        ProjectRecord,
                        PhaseRecord.project_id == ProjectRecord.id,
                    )
                    .where(ProjectRecord.slug == project_slug)
                )

            tasks = list(session.scalars(stmt))
            result = []
            for t in tasks:
                result.append(
                    {
                        "title": t.title,
                        "status": t.status,
                        "owner": t.owner,
                        "phase": t.phase.name if t.phase else None,
                    }
                )
            return json.dumps(result, indent=2)

    @mcp.tool()
    def refresh_source_data() -> str:
        """Refresh source data from markdown trackers and sync to SQLite."""
        if not settings.projects_dir.exists():
            return json.dumps(
                {
                    "error": f"Projects directory not found: {settings.projects_dir}"
                }
            )

        init_db()
        with SessionLocal() as session:
            results = sync_directory(session, settings.projects_dir)
            return json.dumps(
                {
                    "projects": results["projects"],
                    "phases": results["phases"],
                    "tasks": results["tasks"],
                },
                indent=2,
            )
