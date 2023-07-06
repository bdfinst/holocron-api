"""Types."""
from typing import Dict, List, NamedTuple


class DateValue(NamedTuple):
    """DateValue type."""

    date: str
    value: float


ChartData = Dict[str, List[float]]
