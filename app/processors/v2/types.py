"""Types."""
from datetime import datetime
from typing import Dict, List, NamedTuple


class DateValue(NamedTuple):
    """DateValue type."""

    date: datetime
    value: float


WeeklyData = Dict[str, List[float]]
ChartData = Dict[str, WeeklyData]
