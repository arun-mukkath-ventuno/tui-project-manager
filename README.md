# TUI Project Manager

Local-first terminal project manager for markdown-based trackers.

This app reads markdown tracker files (like those in `/project-manager`),
indexes them into SQLite, and presents a fast terminal dashboard with
AI-assisted summaries and MCP-based agent access.

The markdown trackers remain the **source of truth**. This app only reads
them — if SQLite is deleted, it rebuilds from markdown.

Design direction for the UI lives in [docs/design-guideline.md](docs/design-guideline.md).

---

## Features

| Feature | Status |
|---------|--------|
| **TUI Dashboard** | ✅ Interactive project list with status counts |
| **Project Drilldown** | ✅ Phase + task tables with navigation |
| **Task Detail** | ✅ Full task metadata view |
| **Markdown Ingest** | ✅ Parses tracker files into SQLite |
| **CLI Commands** | ✅ `refresh`, `list`, `show`, `summarize` |
| **AI Summaries** | ✅ LLM-generated project summaries via OpenAI-compatible APIs |
| **MCP Server** | ✅ Agent-accessible tools (Claude Desktop, Cursor, etc.) |

---

## Quick Start

### 1. Setup

Requires **Python 3.12** and a virtual environment:

```bash
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure

Copy `.env.example` to `.env` and add your OpenAI-compatible API key:

```bash
cp .env.example .env
```

Edit `.env`:
```
# Required for AI summaries
OPENAI_API_KEY=sk-your-key-here

# Optional: use Groq, Ollama, etc.
# OPENAI_BASE_URL=https://api.groq.com/openai/v1
# OPENAI_MODEL=llama3-70b-8192

# Project trackers directory (auto-detected on this machine)
PROJECTS_DIR=/Users/arunmukkath/Work/project-manager/task-trackers
```

### 3. Sync & Run

```bash
# Ingest markdown trackers into SQLite
vpm-tui refresh

# Launch the TUI dashboard
vpm-tui run
```

---

## CLI Usage

```bash
# Re-sync markdown sources → SQLite
vpm-tui refresh

# List all projects with task counts
vpm-tui list

# Text drilldown of a single project
vpm-tui show web-player

# Generate AI summary for a project
vpm-tui summarize bluekona-content-pipeline

# Start MCP server (stdio transport)
vpm-tui mcp
```

---

## TUI Navigation

```
Dashboard ──Enter──► Project Detail ──Enter──► Task Detail
                    ◄── Escape ──►            ◄── Escape ──►
```

| Key | Action |
|-----|--------|
| `↑↓` | Navigate table rows |
| `Enter` | Drill into selected row |
| `r` | Refresh data from markdown (dashboard) |
| `s` | Generate AI summary (project detail) |
| `Escape` | Go back (pushed screens) |
| `q` | Quit app (anywhere) |

---

## MCP Server

The `vpm-tui mcp` command starts an MCP server over **stdio** — compatible with
Claude Desktop, Cursor, and any MCP client.

Exposed tools:

| Tool | Description |
|------|-------------|
| `list_projects` | JSON array of all projects + task counts |
| `get_project_detail` | Full project with phases and tasks by slug |
| `list_tasks` | All tasks, optionally filtered by project |
| `generate_summary` | AI-generated project summary |
| `refresh_source_data` | Re-sync markdown trackers into SQLite |

### Claude Desktop Config

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vpm-tui": {
      "command": "/Users/arunmukkath/Work/tui-project-manager/.venv/bin/vpm-tui",
      "args": ["mcp"]
    }
  }
}
```

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   TUI       │────►│  Application │────►│   SQLite    │
│  (Textual)  │     │   (Business) │     │  (SQLA 2.0) │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Ingest/Parser│◄── markdown trackers
                    │ (custom regex)│    from /project-manager
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   AI Client  │◄── OpenAI-compatible API
                    │  (Pydantic)  │
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  MCP Server  │──► stdio / Claude Desktop
                    │  (FastMCP)   │
                    └──────────────┘
```

### Domain Model

- **Project** — name, slug, source path, task counts, last synced
- **Phase** — project section (`##`) or subsection (`###`)
- **Task** — title, status, owner, phase reference, source file
- **Summary** — AI-generated: summary text, highlights, blockers, next actions

### Tracker Markdown Format

The parser expects tracker files like:

```markdown
# Project Name — Task Tracker

**Project:** `Project Name`

## Phase 1

- open | 1.1 Task title - Owner Name
- dev-complete | 1.2 Another task

## Phase 2

### Subsection

- wip | 2.1 Sub task
```

Status values: `open`, `wip`, `dev-complete`, `qa-complete`, `in-production`

---

## Development

```bash
# Run all tests
pytest tests/ -v

# Lint check
ruff check src tests

# Auto-fix lint issues
ruff check --fix src tests
```

### Test Suite (13 tests)

| File | Coverage |
|------|----------|
| `test_parser.py` | Markdown header, phase, task, owner, count extraction |
| `test_sync.py` | In-memory SQLite sync: create + upsert |
| `test_db.py` | Repository queries: get_all, get_by_slug, get_with_details |
| `test_mcp.py` | MCP tool registration |
| `test_cli.py` | CLI help smoke test |

---

## Origin

This repo evolved from the markdown tracker workflow in `/project-manager`.
That repository remains the human-authored planning source; this app reads
those files and provides a better working surface for day-to-day navigation,
reporting, and AI-assisted analysis.
