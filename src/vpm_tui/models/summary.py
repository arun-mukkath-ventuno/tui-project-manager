"""Summary domain model."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class Summary(BaseModel):
    """An AI-generated project summary."""

    id: str = Field(..., description="Unique summary identifier")
    project_id: str = Field(..., description="Target project identifier")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    summary_text: str = Field(default="", description="Summary text")
    highlights: list[str] = Field(default_factory=list, description="Key highlights")
    blockers: list[str] = Field(default_factory=list, description="Current blockers")
    suggested_next_actions: list[str] = Field(
        default_factory=list, description="Suggested next actions"
    )
