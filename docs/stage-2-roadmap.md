# Stage 2 Roadmap

Deferred until MVP is stable. Ordered by likely value vs effort.

## High Value

### Write-Back Editing
- Edit task status, owner, title from the TUI and sync back to markdown source
- Requires: markdown AST preservation, git-safe writes, conflict detection

### Watch Mode
- Background filesystem watcher (`watchdog` or `fswatch`) to auto-refresh when markdown changes
- Debounced sync to avoid thrashing

### Richer TUI Widgets
- Collapsible phase panels in project detail
- Search/filter bar across projects and tasks
- Sortable columns in DataTable

### Diff View Between Syncs
- Show what changed since last refresh: new tasks, status changes, completions
- Persist sync snapshots in SQLite for comparison

## Medium Value

### Notifications
- Stale task detection with configurable thresholds (e.g., "open for > 30 days")
- Terminal notification or bell when stale items exist

### Multi-Source Aggregation
- Read from multiple project directories or repos at startup
- Cross-project dashboard view

### MCP Write Tools
- `update_task_status`, `add_task`, `move_task` tools for agent-driven updates
- Tightly controlled: agents can suggest but human approves writes

### Cached AI Summaries
- Store generated summaries in `SummaryRecord` with timestamps
- Invalidate on refresh; allow viewing cached summary without re-calling LLM

## Lower Value / Higher Effort

### PostgreSQL Backend Option
- Swap SQLite for PostgreSQL for teams that want a shared instance
- Requires connection pooling, migrations, deployment story

### Background Sync Service
- Daemon mode with scheduling (cron-like or file watch)
- systemd / launchd integration

### Web UI (Parallel Interface)
- FastHTML or similar lightweight web view of the same SQLite data
- Out of scope for this repo; would be a separate project

### Analytics & Trend Charts
- Historical task completion velocity
- Burndown-style charts per project
- Requires persistent history beyond last-sync snapshot
