"""Project domain model."""

from datetime import datetime

from pydantic import BaseModel, Field


class Project(BaseModel):
    """A project entity."""

    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Display name")
    slug: str = Field(..., description="URL-friendly slug")
    source_path: str = Field(..., description="Path to source markdown file")
    last_synced_at: datetime | None = Field(None, description="Last sync timestamp")
    task_counts: dict[str, int] = Field(default_factory=dict, description="Counts by status")
    notes: str = Field(default="", description="Free-form notes")
