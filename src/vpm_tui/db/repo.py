"""Repository layer for database operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from vpm_tui.db.schema import PhaseRecord, ProjectRecord


class ProjectRepository:
    """Repository for project records."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self) -> list[ProjectRecord]:
        stmt = select(ProjectRecord).order_by(ProjectRecord.name)
        return list(self._session.scalars(stmt))

    def get_by_slug(self, slug: str) -> ProjectRecord | None:
        stmt = select(ProjectRecord).where(ProjectRecord.slug == slug)
        return self._session.scalar(stmt)

    def get_with_details(self, slug: str) -> ProjectRecord | None:
        from sqlalchemy.orm import selectinload

        stmt = (
            select(ProjectRecord)
            .where(ProjectRecord.slug == slug)
            .options(
                selectinload(ProjectRecord.phases).selectinload(PhaseRecord.tasks)
            )
        )
        return self._session.scalar(stmt)
