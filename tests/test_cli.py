"""Tests for CLI commands."""

from typer.testing import CliRunner

from tpman.cli import app

runner = CliRunner()


def test_cli_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "TUI Project Manager" in result.output
