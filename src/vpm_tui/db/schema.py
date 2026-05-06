"""SQLAlchemy ORM schema."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ProjectRecord(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, index=True)
    source_path: Mapped[str] = mapped_column(String, nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(nullable=True)
    task_counts: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    phases: Mapped[list[PhaseRecord]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="PhaseRecord.order",
    )
    summaries: Mapped[list[SummaryRecord]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class PhaseRecord(Base):
    __tablename__ = "phases"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(nullable=False, default=0)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    project: Mapped[ProjectRecord] = relationship(back_populates="phases")
    tasks: Mapped[list[TaskRecord]] = relationship(
        back_populates="phase",
        cascade="all, delete-orphan",
        order_by="TaskRecord.order",
    )


class TaskRecord(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    phase_id: Mapped[str] = mapped_column(ForeignKey("phases.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[str] = mapped_column(String, nullable=False, index=True)
    owner: Mapped[str | None] = mapped_column(String, nullable=True)
    due_date: Mapped[str | None] = mapped_column(String, nullable=True)
    effort: Mapped[str | None] = mapped_column(String, nullable=True)
    source_file: Mapped[str] = mapped_column(String, nullable=False)
    source_line: Mapped[int | None] = mapped_column(nullable=True)
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON

    phase: Mapped[PhaseRecord] = relationship(back_populates="tasks")


class SummaryRecord(Base):
    __tablename__ = "summaries"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    summary_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    highlights: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    blockers: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    suggested_next_actions: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON

    project: Mapped[ProjectRecord] = relationship(back_populates="summaries")
