# Architecture

## Layers

```
┌─────────────────────────────────────────────────────────────┐
│  TUI Layer (Textual)                                          │
│  DashboardScreen → ProjectDetailScreen → TaskDetailScreen   │
│  SummaryPanel | DataTable | Header | Footer                   │
├─────────────────────────────────────────────────────────────┤
│  Application Layer (vpm_tui)                                  │
│  ProjectRepository | Ingest Pipeline | Refresh Flow         │
├─────────────────────────────────────────────────────────────┤
│  Markdown Ingest Layer                                        │
│  find_markdown_files() → parse() → sync_directory()           │
│  Regex-based parser for tracker-style markdown                │
├─────────────────────────────────────────────────────────────┤
│  SQLite Layer (SQLAlchemy 2.0)                                │
│  ProjectRecord | PhaseRecord | TaskRecord | SummaryRecord     │
│  Relationships: Project → Phases → Tasks                      │
├─────────────────────────────────────────────────────────────┤
│  AI Layer (OpenAI-compatible)                                 │
│  AIClient → ProjectSummarizer → JSON prompt/response          │
├─────────────────────────────────────────────────────────────┤
│  MCP Layer (FastMCP stdio)                                    │
│  list_projects | get_project_detail | list_tasks              │
│  generate_summary | refresh_source_data                       │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

1. Human edits markdown trackers in `/project-manager/task-trackers/`
2. `vpm-tui refresh` reads `.md` files, parses headers/phases/tasks/status
3. Normalized data is written to SQLite with cascade replace per project
4. Dashboard and drilldown views render from SQLite
5. AI summaries are generated on demand from the SQLite-indexed task state
6. MCP tools expose the same SQLite-backed read API to agents

## Key Decisions

- **Markdown is source of truth** — SQLite is a derived index; delete it and rebuild
- **No background daemon** — refresh is explicit and on-demand
- **No write-back** — MVP is read-only from markdown; editing happens in the source repo
- **Pydantic models + SQLAlchemy ORM** — domain models for business logic, ORM records for persistence
- **Custom regex parser** — faster and more predictable than full markdown AST for our rigid tracker format
