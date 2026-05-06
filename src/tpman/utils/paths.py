"""Path utilities."""

from pathlib import Path


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists.

    Args:
        path: Directory path.

    Returns:
        The directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path
