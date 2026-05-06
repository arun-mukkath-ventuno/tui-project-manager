"""Tests for database layer."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vpm_tui.db.repo import ProjectRepository
from vpm_tui.db.schema import Base, PhaseRecord, ProjectRecord, TaskRecord


def test_repo_get_all_ordered() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_cls = sessionmaker(bind=engine)

    with session_cls() as session:
        session.add(
            ProjectRecord(
                id="proj-2",
                name="Beta",
                slug="beta",
                source_path="b.md",
                task_counts="{}",
                notes="",
            )
        )
        session.add(
            ProjectRecord(
                id="proj-1",
                name="Alpha",
                slug="alpha",
                source_path="a.md",
                task_counts="{}",
                notes="",
            )
        )
        session.commit()

        repo = ProjectRepository(session)
        projects = repo.get_all()
        assert len(projects) == 2
        assert projects[0].name == "Alpha"
        assert projects[1].name == "Beta"


def test_repo_get_by_slug() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_cls = sessionmaker(bind=engine)

    with session_cls() as session:
        session.add(
            ProjectRecord(
                id="proj-1",
                name="Alpha",
                slug="alpha",
                source_path="a.md",
                task_counts="{}",
                notes="",
            )
        )
        session.commit()

        repo = ProjectRepository(session)
        p = repo.get_by_slug("alpha")
        assert p is not None
        assert p.name == "Alpha"

        missing = repo.get_by_slug("nonexistent")
        assert missing is None


def test_repo_get_with_details() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_cls = sessionmaker(bind=engine)

    with session_cls() as session:
        project = ProjectRecord(
            id="proj-1",
            name="Alpha",
            slug="alpha",
            source_path="a.md",
            task_counts="{}",
            notes="",
        )
        phase = PhaseRecord(
            id="phase-1",
            project_id="proj-1",
            name="Phase 1",
            order=0,
            summary="",
        )
        task = TaskRecord(
            id="task-1",
            phase_id="phase-1",
            title="Do something",
            order=0,
            status="open",
            owner="Arun",
            source_file="a.md",
        )
        session.add_all([project, phase, task])
        session.commit()

        repo = ProjectRepository(session)
        p = repo.get_with_details("alpha")
        assert p is not None
        assert len(p.phases) == 1
        assert len(p.phases[0].tasks) == 1
        assert p.phases[0].tasks[0].title == "Do something"
