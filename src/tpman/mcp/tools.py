"""MCP tools exposed to agents."""


async def list_projects() -> list[dict]:
    """List all projects.

    Returns:
        List of project dicts.
    """
    # TODO: implement
    raise NotImplementedError


async def get_project_detail(slug: str) -> dict:
    """Get project detail.

    Args:
        slug: Project slug.

    Returns:
        Project detail dict.
    """
    # TODO: implement
    raise NotImplementedError


async def list_tasks(project_id: str | None = None) -> list[dict]:
    """List tasks.

    Args:
        project_id: Optional project filter.

    Returns:
        List of task dicts.
    """
    # TODO: implement
    raise NotImplementedError


async def generate_summary(project_id: str) -> str:
    """Generate a project summary.

    Args:
        project_id: Target project.

    Returns:
        Summary text.
    """
    # TODO: implement
    raise NotImplementedError


async def refresh_source_data() -> str:
    """Refresh source data from markdown.

    Returns:
        Status message.
    """
    # TODO: implement
    raise NotImplementedError
