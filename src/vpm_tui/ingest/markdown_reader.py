"""Read markdown files from disk."""

from pathlib import Path


def find_markdown_files(root: Path) -> list[Path]:
    """Recursively find all markdown files under root."""
    return sorted(root.rglob("*.md"))


def read_file(path: Path) -> str:
    """Read file contents as text."""
    return path.read_text(encoding="utf-8")
