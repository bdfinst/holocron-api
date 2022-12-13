"""Time utils module."""

from datetime import datetime


def total_days_diff(start: datetime, end: datetime) -> float:
    """Return the total number of days between two dates."""
    hours_per_day = 24
    seconds_per_day = 60 * 60 * hours_per_day
    time_delta = end - start
    days_diff = time_delta.days + time_delta.seconds / seconds_per_day

    precision_factor = 10
    return round(days_diff * precision_factor) / precision_factor
