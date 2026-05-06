"""Tests for sync pipeline."""

import tempfile
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from vpm_tui.db.schema import Base, PhaseRecord, ProjectRecord, TaskRecord
from vpm_tui.ingest.sync import sync_directory

SAMPLE_MD = """\
# Test Sync — Task Tracker

**Project:** `Test Sync`

## Phase A

- open | 1.1 Task one
- dev-complete | 1.2 Task two
"""


def test_sync_creates_records() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_cls = sessionmaker(bind=engine)

    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = Path(tmpdir) / "TEST_SYNC_TASKS.md"
        md_path.write_text(SAMPLE_MD)

        with session_cls() as session:
            results = sync_directory(session, Path(tmpdir))
            assert results["projects"] == 1
            assert results["phases"] == 1
            assert results["tasks"] == 2

            project = session.get(ProjectRecord, "test-sync")
            assert project is not None
            assert project.name == "Test Sync"

            phases = list(
                session.scalars(
                    select(PhaseRecord).where(
                        PhaseRecord.project_id == "test-sync"
                    )
                )
            )
            assert len(phases) == 1
            assert phases[0].name == "Phase A"

            tasks = list(
                session.scalars(
                    select(TaskRecord).where(
                        TaskRecord.phase_id == phases[0].id
                    )
                )
            )
            assert len(tasks) == 2
            assert tasks[0].title == "Task one"
            assert tasks[0].status == "open"
            assert tasks[0].order == 1
            assert tasks[1].title == "Task two"
            assert tasks[1].status == "dev-complete"
            assert tasks[1].order == 2


def test_sync_upserts_existing() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_cls = sessionmaker(bind=engine)

    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = Path(tmpdir) / "TEST_SYNC_TASKS.md"
        md_path.write_text(SAMPLE_MD)

        with session_cls() as session:
            results1 = sync_directory(session, Path(tmpdir))
            assert results1["projects"] == 1

            results2 = sync_directory(session, Path(tmpdir))
            assert results2["projects"] == 1

            tasks = list(session.scalars(select(TaskRecord)))
            assert len(tasks) == 2
