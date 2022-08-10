"""Processor utils test."""
from datetime import datetime

from pytest import fixture

from app.processors import utils
from app.processors.types import DateValue
from app.processors.utils import days_between_dates, flat_map, values_by_week
from tests.mocks import config


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(utils, "config", config)
    yield config
    config.reset()


def test_flat_map():
    """Test flat_map function."""
    test_cases = [
        {"input": [], "expected": [], "func": lambda x: [x]},
        {
            "input": [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}],
            "expected": [1, 2, 3, 4],
            "func": lambda x: [x["a"]],
        },
    ]
    for case in test_cases:
        expected = case["expected"]
        actual = flat_map(case["input"], case["func"])
        assert len(actual) == len(expected)
        assert all(a == b for a, b in zip(actual, expected))


def test_values_by_week():
    """Test values_by_week function."""
    input_data = [
        DateValue(datetime(year=2000, month=1, day=3), value=1),
        DateValue(datetime(year=2000, month=3, day=6), value=1),
    ]
    expected = {"2000_01": [1], "2000_10": [1]}
    actual = values_by_week(input_data)
    assert expected == actual


def test_days_between_dates(mock_config):
    """Test days_between_dates function."""
    mock_config.MIN_EXPECTED_CYCLE_TIME_HOURS = 1

    cases = [
        {
            "start": datetime(year=2000, month=1, day=3),
            "end": datetime(year=2000, month=1, day=9),
            "expected": 5,
        },
        {
            "start": datetime(year=2000, month=1, day=3, minute=30),
            "end": datetime(year=2000, month=1, day=3, minute=45),
            "expected": 0,
        },
    ]
    for case in cases:
        actual = days_between_dates(case["start"], case["end"])
        expected = case["expected"]
        assert actual == expected
