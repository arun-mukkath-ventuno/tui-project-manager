"""Date utilities."""

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(UTC)


def parse_date(value: str | None) -> datetime | None:
    """Parse a date string.

    Args:
        value: Date string.

    Returns:
        Parsed datetime or None.
    """
    if not value:
        return None
    # TODO: implement parsing
    raise NotImplementedError
