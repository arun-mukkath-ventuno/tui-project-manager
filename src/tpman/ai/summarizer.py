"""AI summarizer for projects."""

import json
import re
from datetime import UTC, datetime

from tpman.ai.client import AIClient
from tpman.db.repo import ProjectRepository
from tpman.db.session import SessionLocal
from tpman.models.summary import Summary


class ProjectSummarizer:
    """Generate AI summaries for projects."""

    def __init__(self, client: AIClient | None = None) -> None:
        self.client = client or AIClient()

    def summarize(self, project_id: str) -> Summary:
        """Generate a summary for a project.

        Args:
            project_id: Target project identifier (slug).

        Returns:
            Summary model with structured AI output.
        """
        with SessionLocal() as session:
            repo = ProjectRepository(session)
            project = repo.get_with_details(project_id)
            if not project:
                raise ValueError(f"Project '{project_id}' not found")

            counts = json.loads(project.task_counts or "{}")
            total = sum(counts.values())

            open_tasks: list[str] = []
            wip_tasks: list[str] = []
            dev_complete_tasks: list[str] = []

            for phase in project.phases:
                for task in phase.tasks:
                    line = f"- [{phase.name}] {task.title}"
                    if task.owner:
                        line += f" ({task.owner})"
                    if task.status == "open":
                        open_tasks.append(line)
                    elif task.status == "wip":
                        wip_tasks.append(line)
                    elif task.status == "dev-complete":
                        dev_complete_tasks.append(line)

            prompt = self._build_prompt(
                project_name=project.name,
                total=total,
                counts=counts,
                open_tasks=open_tasks,
                wip_tasks=wip_tasks,
                dev_complete_tasks=dev_complete_tasks,
            )

            response = self.client.chat(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior engineering manager analyzing "
                            "project status. Respond only with valid JSON."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            data = self._parse_json(response)

            return Summary(
                id=f"{project_id}-{datetime.now(UTC).isoformat()}",
                project_id=project_id,
                generated_at=datetime.now(UTC),
                summary_text=data.get("summary_text", ""),
                highlights=data.get("highlights", []),
                blockers=data.get("blockers", []),
                suggested_next_actions=data.get("suggested_next_actions", []),
            )

    def _build_prompt(
        self,
        project_name: str,
        total: int,
        counts: dict[str, int],
        open_tasks: list[str],
        wip_tasks: list[str],
        dev_complete_tasks: list[str],
    ) -> str:
        open_text = "\n".join(open_tasks[:20]) or "None"
        wip_text = "\n".join(wip_tasks[:20]) or "None"
        done_text = "\n".join(dev_complete_tasks[:20]) or "None"

        return (
            f"Analyze this software project and return structured JSON.\n\n"
            f"Project: {project_name}\n"
            f"Total tasks: {total}\n"
            f"Status breakdown:\n"
            f"- open: {counts.get('open', 0)}\n"
            f"- wip: {counts.get('wip', 0)}\n"
            f"- dev-complete: {counts.get('dev-complete', 0)}\n"
            f"- qa-complete: {counts.get('qa-complete', 0)}\n"
            f"- in-production: {counts.get('in-production', 0)}\n\n"
            f"Open tasks ({len(open_tasks)}):\n{open_text}\n\n"
            f"WIP tasks ({len(wip_tasks)}):\n{wip_text}\n\n"
            f"Dev-complete tasks ({len(dev_complete_tasks)}):\n{done_text}\n\n"
            f"Return JSON with this exact structure:\n"
            f"{{\n"
            f'  "summary_text": "2-3 sentence executive summary",\n'
            f'  "highlights": ["what is going well", "another positive"],\n'
            f'  "blockers": ["risk or blocker 1", "risk or blocker 2"],\n'
            f'  "suggested_next_actions": ["action 1", "action 2", "action 3"]\n'
            f"}}"
        )

    def _parse_json(self, text: str) -> dict:
        """Extract JSON from an LLM response, handling markdown code blocks."""
        # Try direct parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try markdown code block
        match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL
        )
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        # Try finding any JSON object
        match = re.search(r"(\{.*?\})", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        return {}
