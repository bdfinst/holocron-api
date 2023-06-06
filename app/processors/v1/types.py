"""Types."""
from datetime import datetime
from typing import Dict, List, NamedTuple, Union


class DateValue(NamedTuple):
    """DateValue type."""

    date: datetime
    value: Union[int, float]


WeeklyData = Dict[str, List[Union[int, float]]]
ChartData = Dict[str, WeeklyData]
