"""Sync markdown sources into the SQLite index."""

import json
from pathlib import Path

from sqlalchemy.orm import Session

from vpm_tui.db.engine import engine
from vpm_tui.db.schema import Base, PhaseRecord, ProjectRecord, TaskRecord
from vpm_tui.ingest.markdown_reader import find_markdown_files, read_file
from vpm_tui.ingest.parser import MarkdownParser


def init_db() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def sync_directory(session: Session, root: Path) -> dict[str, int]:
    """Read all markdown under root and sync into the database."""
    parser = MarkdownParser()
    results = {"projects": 0, "phases": 0, "tasks": 0}

    for md_path in find_markdown_files(root):
        content = read_file(md_path)
        project, phases, tasks = parser.parse(str(md_path), content)

        existing = session.get(ProjectRecord, project.id)
        if existing:
            session.delete(existing)
            session.flush()

        session.add(
            ProjectRecord(
                id=project.id,
                name=project.name,
                slug=project.slug,
                source_path=project.source_path,
                last_synced_at=project.last_synced_at,
                task_counts=json.dumps(project.task_counts),
                notes="",
            )
        )

        for phase in phases:
            session.add(
                PhaseRecord(
                    id=phase.id,
                    project_id=phase.project_id,
                    name=phase.name,
                    order=phase.order,
                    summary=phase.summary,
                )
            )

        for task in tasks:
            session.add(
                TaskRecord(
                    id=task.id,
                    phase_id=task.phase_id,
                    title=task.title,
                    order=task.order,
                    status=task.status,
                    owner=task.owner,
                    due_date=None,
                    effort=None,
                    source_file=task.source_file,
                    source_line=None,
                    tags=None,
                )
            )

        results["projects"] += 1
        results["phases"] += len(phases)
        results["tasks"] += len(tasks)

    session.commit()
    return results
