"""Task domain model."""

from datetime import date

from pydantic import BaseModel, Field


class Task(BaseModel):
    """A task entity."""

    id: str = Field(..., description="Unique task identifier")
    phase_id: str = Field(..., description="Parent phase identifier")
    title: str = Field(..., description="Task title")
    order: int = Field(default=0, description="Display order")
    status: str = Field(default="open", description="Current status")
    owner: str | None = Field(None, description="Assigned owner")
    due_date: date | None = Field(None, description="Due date")
    effort: str | None = Field(None, description="Estimated effort")
    source_file: str = Field(..., description="Source markdown file")
    source_line: int | None = Field(None, description="Line reference")
    tags: list[str] = Field(default_factory=list, description="Tags")
