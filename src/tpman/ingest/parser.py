"""Parse markdown project trackers into normalized structures."""

import re
from datetime import datetime

from tpman.models.phase import Phase
from tpman.models.project import Project
from tpman.models.task import Task

_TASK_LINE_RE = re.compile(
    r"^- \s*(open|wip|dev-complete|qa-complete|in-production)\s*\|\s*(.+)$"
)
_NUMBER_RE = re.compile(r"^(\d+(?:\.\d+)?)\s+(.+)$")
_OWNER_RE = re.compile(r"[-–—]\s*(.+)$")
_SKIP_PHASES = {"progress", "state legend"}


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


class MarkdownParser:
    """Parser for markdown tracker files."""

    def parse(
        self, source_path: str, content: str
    ) -> tuple[Project, list[Phase], list[Task]]:
        """Parse content into a project, phases, and tasks."""
        lines = content.splitlines()

        project_name = self._extract_project_name(lines)

        project = Project(
            id=_slugify(project_name),
            name=project_name,
            slug=_slugify(project_name),
            source_path=source_path,
            last_synced_at=datetime.now(),
            task_counts={},
            notes="",
        )

        phases: list[Phase] = []
        tasks: list[Task] = []
        current_phase: Phase | None = None
        parent_phase_name = ""
        phase_order = 0
        task_order = 0

        for line in lines:
            stripped = line.strip()

            if not stripped or stripped == "---":
                continue

            # Phase header (##)
            if stripped.startswith("## ") and not stripped.startswith("## State Legend"):
                phase_name = stripped[3:].strip()
                if _slugify(phase_name) in _SKIP_PHASES:
                    current_phase = None
                    continue

                phase_order += 1
                parent_phase_name = phase_name
                current_phase = Phase(
                    id=f"{project.id}/phase-{phase_order}",
                    project_id=project.id,
                    name=phase_name,
                    order=phase_order,
                    summary="",
                )
                phases.append(current_phase)
                task_order = 0

            # Subsection (###) — creates a new sub-phase
            elif stripped.startswith("### ") and current_phase is not None:
                subsection_name = stripped[4:].strip()
                phase_order += 1
                current_phase = Phase(
                    id=f"{project.id}/phase-{phase_order}",
                    project_id=project.id,
                    name=f"{parent_phase_name} / {subsection_name}",
                    order=phase_order,
                    summary="",
                )
                phases.append(current_phase)
                task_order = 0

            # Task line
            elif stripped.startswith("- ") and current_phase is not None:
                task_match = _TASK_LINE_RE.match(stripped)
                if task_match:
                    status = task_match.group(1)
                    rest = task_match.group(2).strip()

                    # Extract optional task number (e.g. 1.1, 0.5)
                    number_match = _NUMBER_RE.match(rest)
                    if number_match:
                        desc_rest = number_match.group(2).strip()
                    else:
                        desc_rest = rest

                    # Extract optional owner from trailing " - Name"
                    owner_match = _OWNER_RE.search(desc_rest)
                    if owner_match:
                        task_owner = owner_match.group(1).strip()
                        description = desc_rest[: owner_match.start()].strip()
                    else:
                        task_owner = None
                        description = desc_rest

                    task_order += 1
                    task_id = f"{current_phase.id}/task-{task_order}"

                    tasks.append(
                        Task(
                            id=task_id,
                            phase_id=current_phase.id,
                            title=description,
                            order=task_order,
                            status=status,
                            owner=task_owner,
                            due_date=None,
                            effort=None,
                            source_file=source_path,
                            source_line=None,
                            tags=[],
                        )
                    )

        # Compute per-status counts
        counts: dict[str, int] = {}
        for task in tasks:
            counts[task.status] = counts.get(task.status, 0) + 1
        project.task_counts = counts

        return project, phases, tasks

    def _extract_project_name(self, lines: list[str]) -> str:
        for line in lines:
            match = re.match(r"^\*\*Project:\*\*\s*`(.+?)`", line.strip())
            if match:
                return match.group(1)
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip().replace(" — Task Tracker", "")
        return "unknown"
