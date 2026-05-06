"""AI summarizer for projects."""

from tpman.ai.client import AIClient


class ProjectSummarizer:
    """Generate AI summaries for projects."""

    def __init__(self, client: AIClient | None = None) -> None:
        self.client = client or AIClient()

    def summarize(self, project_id: str) -> str:
        """Generate a summary for a project.

        Args:
            project_id: Target project identifier.

        Returns:
            Summary text.
        """
        # TODO: implement
        raise NotImplementedError
