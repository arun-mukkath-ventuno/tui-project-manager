"""Phase domain model."""

from pydantic import BaseModel, Field


class Phase(BaseModel):
    """A project phase."""

    id: str = Field(..., description="Unique phase identifier")
    project_id: str = Field(..., description="Parent project identifier")
    name: str = Field(..., description="Phase name")
    order: int = Field(default=0, description="Phase order")
    summary: str = Field(default="", description="Phase summary")
