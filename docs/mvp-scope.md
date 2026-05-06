# MVP Scope

## Implemented ✅

### Core
- [x] Repo scaffolding with Python 3.12, `src/vpm_tui/`
- [x] `pyproject.toml` with dependencies and `vpm-tui` CLI entry point
- [x] Pydantic `Settings` with `.env` loading (pydantic-settings)
- [x] SQLAlchemy 2.0 ORM schema: Project, Phase, Task, Summary
- [x] SQLite persistence with relationships and `order_by` on collections
- [x] Repository pattern for DB queries

### Markdown Ingest
- [x] `find_markdown_files()` — recursive `.md` discovery
- [x] Regex-based parser: headers, `##` phases, `###` subsections, task lines
- [x] Status extraction: `open`, `wip`, `dev-complete`, `qa-complete`, `in-production`
- [x] Owner extraction from trailing ` - Name`
- [x] Task numbering detection (`1.1`, `0.5`)
- [x] Skip sections: `Progress`, `State Legend`
- [x] Sync pipeline with atomic delete/replace per project

### TUI
- [x] Dashboard screen: DataTable with project list and status counts
- [x] Project Detail screen: phases + tasks table, AI summary panel
- [x] Task Detail screen: full metadata (title, status, owner, phase, project, source)
- [x] Navigation: `↑↓` + `Enter` to drill, `Escape` to go back, `q` to quit
- [x] In-app refresh (`r` on dashboard)
- [x] AI summary generation (`s` on project detail)
- [x] `cursor_type="row"` on DataTables for reliable row selection

### CLI
- [x] `vpm-tui run` — launch TUI
- [x] `vpm-tui refresh` — sync markdown → SQLite
- [x] `vpm-tui list` — print project list
- [x] `vpm-tui show <slug>` — text drilldown
- [x] `vpm-tui summarize <slug>` — LLM-generated summary
- [x] `vpm-tui mcp` — start MCP stdio server

### AI
- [x] OpenAI-compatible client wrapper (supports custom base_url + model)
- [x] Structured JSON prompt with task breakdown
- [x] Response parsing with markdown-codeblock fallback
- [x] Summary model: summary_text, highlights, blockers, next_actions

### MCP
- [x] FastMCP stdio server
- [x] 5 read tools: list_projects, get_project_detail, list_tasks, generate_summary, refresh_source_data

### Tests
- [x] 13 tests: parser, sync, db, mcp, cli
- [x] ruff linting + auto-fix

## Explicitly Out of Scope

- No write-back editing from TUI to markdown
- No background daemon / watch mode
- No PostgreSQL or Redis
- No multi-user collaboration
- No web UI
- No auth or permissions
