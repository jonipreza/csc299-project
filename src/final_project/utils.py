"""Utility helpers for final_project.

TODOs:
- `generate_id(prefix)` - unique id generator
- `iso_now()` - ISO timestamp helper
- `parse_date(text)` - lightweight date parser
"""

from datetime import datetime, timezone
import uuid
from typing import Optional


def generate_id(prefix: str = "t") -> str:
    """Return a short unique id using a prefix and uuid4 hex.

    TODO: make collision-resistant if needed.
    """
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def iso_now() -> str:
    """Return current time as an ISO 8601 string in UTC (timezone-aware).

    Uses a timezone-aware UTC timestamp to avoid deprecated naive UTC.
    """
    return datetime.now(timezone.utc).isoformat()


def parse_date(text: str) -> Optional[datetime]:
    """Try parsing a date string. Returns a datetime or None.

    This supports ISO 8601 strings (with or without offset). For more
    flexible parsing consider `dateparser` or `pendulum` in the future.
    """
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except Exception:
        return None
