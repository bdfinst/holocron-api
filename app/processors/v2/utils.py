"""Utilities."""
from datetime import datetime, timedelta
from typing import List

from .types import DateValue, WeeklyData


def get_monday_string(date: datetime) -> str:
    """Return the formatted YYYY-MM-DD of the date's week's Monday."""
    monday = date - timedelta(days=date.weekday())
    date_format = "%Y-%m-%d"
    return monday.strftime(date_format)


def values_by_week(data: List[DateValue]) -> WeeklyData:
    """Convert data to format the charts can consume."""
    values: WeeklyData = {}

    for item in data:
        date_str = get_monday_string(item.date)
        values.setdefault(date_str, []).append(item.value)

    return values


def average(numbers: List[float], default: float = 0) -> float:
    """Get average of list of numbers."""
    return default if not numbers else sum(numbers) / len(numbers)
