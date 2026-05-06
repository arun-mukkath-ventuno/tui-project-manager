"""Summary panel widget."""

from textual.widgets import Static

from vpm_tui.models.summary import Summary


class SummaryPanel(Static):
    """Widget to display AI-generated summaries."""

    def on_mount(self) -> None:
        self.add_class("summary-panel")
        self.update("[dim]Press [b]s[/b] to generate AI summary[/dim]")

    def show_summary(self, summary: Summary) -> None:
        """Render a Summary model into the panel."""
        lines = ["[b]Summary[/b]", f"{summary.summary_text}", ""]

        if summary.highlights:
            lines.extend(
                ["[green]✓ Highlights:[/green]"]
                + [f"  • {h}" for h in summary.highlights]
            )

        if summary.blockers:
            lines.extend(
                ["", "[yellow]⚠ Blockers:[/yellow]"]
                + [f"  • {b}" for b in summary.blockers]
            )

        if summary.suggested_next_actions:
            lines.extend(
                ["", "[blue]→ Next Actions:[/blue]"]
                + [f"  • {a}" for a in summary.suggested_next_actions]
            )

        self.update("\n".join(lines))

    def show_error(self, message: str) -> None:
        """Display an error message."""
        self.update(f"[red]Error: {message}[/red]")

    def show_loading(self) -> None:
        """Display a loading indicator."""
        self.update("[dim]Generating summary...[/dim]")
