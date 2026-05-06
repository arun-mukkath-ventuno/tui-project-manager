"""Tests for markdown parser."""

from tpman.ingest.parser import MarkdownParser

SAMPLE_TRACKER = """\
# Test Project — Task Tracker

**Project:** `Test Project`

## Phase 1

- open | 1.1 First task - Arun
- dev-complete | 1.2 Second task

## Phase 2

### Subsection A

- wip | 2.1 Sub task
- open | 2.2 Another sub task - Rajan

## Progress

| Category | Total | Done | Remaining |
|---|---|---|---|
| Phase 1 | 2 | 1 | 1 |
| **Total** | **2** | **1** | **1** |

## State Legend
- `open`
- `wip`
- `dev-complete`
"""


def test_parser_extracts_project() -> None:
    parser = MarkdownParser()
    project, phases, tasks = parser.parse("test.md", SAMPLE_TRACKER)
    assert project.name == "Test Project"
    assert project.slug == "test-project"


def test_parser_extracts_phases() -> None:
    parser = MarkdownParser()
    project, phases, tasks = parser.parse("test.md", SAMPLE_TRACKER)
    assert len(phases) == 3
    assert phases[0].name == "Phase 1"
    assert phases[1].name == "Phase 2"
    assert phases[2].name == "Phase 2 / Subsection A"


def test_parser_extracts_tasks() -> None:
    parser = MarkdownParser()
    project, phases, tasks = parser.parse("test.md", SAMPLE_TRACKER)
    assert len(tasks) == 4

    assert tasks[0].title == "First task"
    assert tasks[0].status == "open"
    assert tasks[0].owner == "Arun"
    assert tasks[0].order == 1

    assert tasks[1].title == "Second task"
    assert tasks[1].status == "dev-complete"
    assert tasks[1].owner is None
    assert tasks[1].order == 2

    assert tasks[2].title == "Sub task"
    assert tasks[2].status == "wip"
    assert tasks[2].order == 1

    assert tasks[3].title == "Another sub task"
    assert tasks[3].owner == "Rajan"
    assert tasks[3].order == 2


def test_parser_task_counts() -> None:
    parser = MarkdownParser()
    project, phases, tasks = parser.parse("test.md", SAMPLE_TRACKER)
    assert project.task_counts == {
        "open": 2,
        "wip": 1,
        "dev-complete": 1,
    }


def test_parser_skips_progress_and_legend() -> None:
    parser = MarkdownParser()
    project, phases, tasks = parser.parse("test.md", SAMPLE_TRACKER)
    phase_names = [p.name for p in phases]
    assert "Progress" not in phase_names
    assert "State Legend" not in phase_names
