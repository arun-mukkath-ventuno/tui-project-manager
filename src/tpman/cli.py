"""CLI commands for tpman."""

import typer

app = typer.Typer(
    name="tpman",
    help="TUI Project Manager",
    no_args_is_help=True,
)


@app.command()
def run() -> None:
    """Launch the TUI."""
    from tpman.app import TpmApp

    TpmApp().run()


@app.command()
def refresh() -> None:
    """Re-read markdown and sync SQLite."""

    from tpman.config import settings
    from tpman.db.session import SessionLocal
    from tpman.ingest.sync import init_db, sync_directory

    if not settings.projects_dir.exists():
        typer.echo(f"Projects directory not found: {settings.projects_dir}")
        raise typer.Exit(1)

    init_db()
    with SessionLocal() as session:
        results = sync_directory(session, settings.projects_dir)
        typer.echo(
            f"Synced {results['projects']} projects, {results['phases']} phases, "
            f"{results['tasks']} tasks"
        )


@app.command("list")
def list_projects() -> None:
    """Print project list in the terminal."""
    import json

    from tpman.db.repo import ProjectRepository
    from tpman.db.session import SessionLocal

    with SessionLocal() as session:
        repo = ProjectRepository(session)
        projects = repo.get_all()
        if not projects:
            typer.echo("No projects found. Run 'tpman refresh' first.")
            return

        for p in projects:
            counts = json.loads(p.task_counts or "{}")
            total = sum(counts.values())
            typer.echo(
                f"{p.name:30} {total:3} tasks  "
                f"open={counts.get('open', 0)} wip={counts.get('wip', 0)} "
                f"done={counts.get('dev-complete', 0)}"
            )


@app.command()
def show(project: str) -> None:
    """Show a project drilldown in text form."""
    import json

    from tpman.db.repo import ProjectRepository
    from tpman.db.session import SessionLocal

    with SessionLocal() as session:
        repo = ProjectRepository(session)
        p = repo.get_by_slug(project)
        if not p:
            typer.echo(f"Project '{project}' not found.")
            raise typer.Exit(1)

        counts = json.loads(p.task_counts or "{}")
        typer.echo(f"Project: {p.name}")
        typer.echo(f"Source:  {p.source_path}")
        typer.echo(f"Synced:  {p.last_synced_at}")
        typer.echo(f"Tasks:   {sum(counts.values())}")
        for status, count in counts.items():
            typer.echo(f"  {status}: {count}")


@app.command()
def summarize(project: str) -> None:
    """Generate a project summary via LLM."""

    from tpman.ai.summarizer import ProjectSummarizer
    from tpman.config import settings
    from tpman.db.repo import ProjectRepository
    from tpman.db.session import SessionLocal

    if not settings.openai_api_key:
        typer.echo(
            "Error: OPENAI_API_KEY not set. "
            "Add it to .env or export OPENAI_API_KEY=sk-..."
        )
        raise typer.Exit(1)

    with SessionLocal() as session:
        repo = ProjectRepository(session)
        p = repo.get_by_slug(project)
        if not p:
            typer.echo(f"Project '{project}' not found.")
            raise typer.Exit(1)

        summarizer = ProjectSummarizer()
        try:
            summary = summarizer.summarize(p.id)
        except Exception as e:
            typer.echo(f"Error generating summary: {e}")
            raise typer.Exit(1)

        typer.echo(f"\n{'=' * 60}")
        typer.echo(f"  Summary: {p.name}")
        typer.echo(f"{'=' * 60}\n")
        typer.echo(summary.summary_text)

        if summary.highlights:
            typer.echo("\n  ✓ Highlights:")
            for item in summary.highlights:
                typer.echo(f"      • {item}")

        if summary.blockers:
            typer.echo("\n  ⚠ Blockers:")
            for item in summary.blockers:
                typer.echo(f"      • {item}")

        if summary.suggested_next_actions:
            typer.echo("\n  → Next Actions:")
            for item in summary.suggested_next_actions:
                typer.echo(f"      • {item}")

        typer.echo()


@app.command()
def mcp() -> None:
    """Start the MCP server."""
    from tpman.mcp.server import main as mcp_main

    mcp_main()


def main() -> None:
    app()
