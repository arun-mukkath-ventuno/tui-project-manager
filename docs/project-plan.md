# TUI Project Manager - Project Plan

## Overview

This project is a local-first terminal application for managing multiple markdown-based project trackers.
It is designed to give a fast dashboard, project drilldown, AI-assisted summaries, and MCP-based agent access
while keeping markdown as the source of truth.

The app is intentionally separate from the existing `project-manager` repository.
That repository remains the human-authored planning source. This app reads those markdown files, indexes them
into SQLite, and presents a better working surface for day-to-day project navigation and reporting.

This plan is based on the markdown tracker system in `/project-manager`, so any future agent or contributor
can trace the app's origin back to that repo and understand that the TUI evolved from the existing tracker
workflow rather than being a standalone greenfield product.

## Product Goals

- Provide a terminal dashboard for project status at a glance
- Support fast drilldown into project, phase, and task detail
- Refresh state from markdown sources on demand
- Keep markdown as the source of truth
- Use SQLite as a derived index for fast querying and history
- Add optional AI summaries and guidance
- Expose MCP tools so agents can read and act on project data

## Non-Goals for MVP

- No remote multi-user collaboration
- No web UI
- No PostgreSQL
- No Redis
- No background daemon
- No auth system
- No complex permissions model
- No write-back editing in the first pass unless explicitly added later

## Repository Model

The app should live in a separate repository, for example:

```text
tui-project-manager/
```

The markdown project trackers remain in a separate repository and are treated as the source-of-truth input.
The TUI repo only reads from those files and stores derived state in SQLite.

## Source of Truth and Data Flow

The system should follow this flow:

1. Human updates markdown files in the planning repo
2. The TUI app reads and parses the markdown source
3. The app normalizes projects, phases, tasks, statuses, and metadata
4. The normalized data is written to SQLite
5. The dashboard and drilldown views render from SQLite
6. AI and MCP features operate on the indexed data
7. Refresh re-runs the ingest flow and updates the derived state

This keeps the app resilient:
- if SQLite is deleted, it can be rebuilt from markdown
- if AI is unavailable, the dashboard still works
- if MCP is offline, the TUI still works

## Recommended Stack

- Python 3.12
- Textual for the TUI
- Rich for tables, formatting, and visual polish
- Typer for CLI commands
- Pydantic for typed models and validation
- SQLAlchemy with SQLite for persistence
- markdown-it-py or a small custom parser for tracker-style markdown
- python-dotenv for configuration
- pytest for tests
- ruff for linting and formatting
- OpenAI-compatible client wrapper for AI summaries
- MCP Python SDK for agent access

## Architecture

### 1. TUI Layer

Responsibilities:
- dashboard screen
- project drilldown screen
- task detail screen
- refresh trigger
- search/filter actions
- summary panel display

### 2. Application Layer

Responsibilities:
- coordinate markdown ingest
- normalize project/task structures
- build summary data
- trigger refreshes
- expose business actions used by the TUI, CLI, AI, and MCP layers

### 3. Markdown Ingest Layer

Responsibilities:
- read markdown files from configured source directories
- detect projects, headers, sections, tasks, and status labels
- convert source files into normalized records
- capture file metadata such as modified time and file path

### 4. SQLite Layer

Responsibilities:
- persist normalized project/task records
- support search and filtering
- store ingest timestamps and version history
- store AI-generated summaries if desired

### 5. AI Layer

Responsibilities:
- summarize project state
- identify stale tasks
- generate next-step suggestions
- provide natural-language drilldown summaries

AI outputs should remain advisory. The markdown source and SQLite index are still the authoritative state.

### 6. MCP Layer

Responsibilities:
- expose tools for external agents
- allow agents to read project state
- allow agents to request refreshes and summaries
- optionally allow controlled updates later

## Proposed Folder Structure

```text
tui-project-manager/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── src/
│   └── vpm_tui/
│       ├── __init__.py
│       ├── app.py
│       ├── cli.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── project.py
│       │   ├── task.py
│       │   └── summary.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── engine.py
│       │   ├── session.py
│       │   ├── schema.py
│       │   └── repo.py
│       ├── ingest/
│       │   ├── __init__.py
│       │   ├── markdown_reader.py
│       │   ├── parser.py
│       │   └── sync.py
│       ├── tui/
│       │   ├── __init__.py
│       │   ├── screens/
│       │   │   ├── __init__.py
│       │   │   ├── dashboard.py
│       │   │   ├── project_detail.py
│       │   │   └── task_detail.py
│       │   └── widgets/
│       │       ├── __init__.py
│       │       ├── project_list.py
│       │       ├── task_table.py
│       │       └── summary_panel.py
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── client.py
│       │   └── summarizer.py
│       ├── mcp/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   └── tools.py
│       └── utils/
│           ├── __init__.py
│           ├── paths.py
│           ├── dates.py
│           └── logging.py
├── data/
│   └── project-manager.db
├── projects/
│   ├── bluekona/
│   ├── bespoke/
│   ├── web-player/
│   └── ott-web-nextjs/
├── tests/
│   ├── test_parser.py
│   ├── test_sync.py
│   ├── test_db.py
│   └── test_ai.py
└── docs/
    ├── project-plan.md
    ├── architecture.md
    ├── mvp-scope.md
    └── stage-2-roadmap.md
```

## Domain Model

### Project

Fields:
- id
- name
- slug
- source path
- last synced at
- task counts by status
- notes

### Phase

Fields:
- id
- project id
- name
- order
- summary

### Task

Fields:
- id
- phase id
- title
- status
- owner
- due date
- effort
- source file
- source line reference if available
- tags

### Summary

Fields:
- id
- project id
- generated at
- summary text
- highlights
- blockers
- suggested next actions

## MVP Screens

### Dashboard

Primary content:
- project list
- status counts
- recently updated projects
- blocked or stale items
- quick refresh action

### Project Drilldown

Primary content:
- project overview
- phase breakdown
- task list by status
- counts per phase
- source file metadata
- AI summary panel

### Task Detail

Primary content:
- task title
- status
- owner
- due date
- source reference
- notes
- related summary or suggestion

## UI Direction

The current UI is functional, but it should be redesigned to feel more deliberate
and more polished than a standard terminal admin table. The goal is clearer
hierarchy, faster scanning, and a stronger product identity.

### Visual Language

- Use a dark, high-contrast palette with one primary accent color
- Keep status colors consistent across the app
- Reserve bright colors for active selection, warnings, and important emphasis
- Use spacing and panels to create clear visual separation between sections
- Avoid default-looking table-heavy layouts where a richer treatment is possible

### Dashboard Treatment

- Add a stronger hero/header band with project count and last sync state
- Make project rows feel more like cards or structured tiles
- Render status counts as compact badges or chips
- Add a visible stale/recent indicator
- Make the selected project state obvious without relying on color alone

### Drilldown Treatment

- Use a split layout when the terminal size allows it
- Keep the summary panel visually distinct from the task table
- Render phase headers as group separators
- Surface owner, status, and due date as small metadata elements
- Give WIP and blocker states more visual weight than completed items

### Task Detail Treatment

- Use label/value grouping with stronger typographic hierarchy
- Surface task status and ownership first
- Keep source metadata visible but secondary
- Leave room for notes, history, or audit context later

### Motion and Feedback

- Add subtle loading and refresh feedback
- Make AI summary generation feel like an intentional action
- Use light transition polish between dashboard and detail views

### UI Polish Tasks

- Add custom Textual CSS for spacing, palette, and typography
- Introduce reusable status badges
- Improve empty states so the UI still feels designed when data is sparse
- Add a dashboard top band with counts and sync metadata
- Differentiate active panes and selected rows more clearly

## MVP Commands

- `vpm-tui run`
  - launch the TUI
- `vpm-tui refresh`
  - re-read markdown and sync SQLite
- `vpm-tui list`
  - print project list in the terminal
- `vpm-tui show <project>`
  - show a project drilldown in text form
- `vpm-tui summarize <project>`
  - generate a project summary
- `vpm-tui mcp`
  - start the MCP server

## MVP Feature Set

### 1. Markdown ingest

The first implementation should parse existing project markdown trackers into normalized data.
This should handle:
- project titles
- section headers
- task lines
- status markers
- simple owner labels

### 2. Dashboard

The dashboard should display:
- project name
- open / wip / dev-complete / qa-complete / in-production counts
- total tasks
- recent refresh status

### 3. Drilldown

The drilldown should let the user select a project and inspect:
- phases
- tasks
- owners
- source file references
- summary notes

### 4. Refresh

Refresh should:
- re-read markdown files
- update SQLite
- preserve prior sync timestamps
- report parsing issues clearly

### 5. AI Summary

AI should be used for:
- project summary
- next-step suggestions
- stale-task detection

AI should not:
- change the source of truth
- auto-edit markdown in MVP

### 6. MCP Tools

MCP should expose read-focused tools first:
- list projects
- get project detail
- list tasks
- generate summary
- refresh source data

Write operations can be added later if needed.

## Stage 2 Ideas

Stage 2 should be deferred until the MVP is stable.

Possible Stage 2 additions:
- configurable source roots instead of a fixed tracker path
- stable project identity separate from display slug
- more tolerant or pluggable markdown parsing
- incremental sync instead of delete-and-reinsert on every refresh
- persisted sync history and source hashing
- typed MCP response schemas instead of raw JSON strings
- clearer AI summary contracts and summary caching
- real end-to-end tests with tracker fixtures from `/project-manager`
- MCP integration tests for read and refresh tools
- UI visual polish and layout refinement
- custom Textual styling system
- richer dashboard cards and section hierarchy
- split-pane drilldown refinement
- task detail card treatment
- write-back editing from the TUI
- task updates from MCP
- Redis cache
- PostgreSQL backend option
- background sync service
- watch mode
- multi-source aggregation
- richer analytics and trend charts
- notifications for stale work
- diff view between sync runs

## Risks and Constraints

- Markdown formats may drift between project files
- Some project docs may use inconsistent status labels
- Parsing rules need to be tolerant, not brittle
- AI output must stay advisory
- MCP write actions should be tightly controlled if added later
- The app should remain useful even if AI or MCP is offline

## Delivery Milestones

### Milestone 1
- repo scaffolding
- config and CLI skeleton
- markdown parser prototype

### Milestone 2
- SQLite schema
- ingest pipeline
- dashboard view

### Milestone 3
- project drilldown
- task detail view
- refresh flow

### Milestone 4
- AI summary integration
- MCP read tools
- polish and tests

## Open Questions

- Which markdown tracker formats must be supported first?
- Should the app read from one repo or multiple repos at startup?
- Which data should be persisted beyond a sync snapshot?
- Do you want read-only MCP in MVP, or do you want controlled write support later?
- Should AI summaries be cached in SQLite or generated on demand?

## Immediate Next Step

Build the repo skeleton with:
- `pyproject.toml`
- `src/vpm_tui/`
- `docs/`
- `tests/`
- a minimal `README.md`

Then implement:
- markdown ingest
- SQLite schema
- dashboard TUI
- refresh command
