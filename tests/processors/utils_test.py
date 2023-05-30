"""Processor utils test."""
from datetime import datetime

from pytest import fixture, raises

from app.processors import utils
from app.processors.types import DateValue
from app.processors.utils import (
    days_between_dates,
    flat_map,
    get_fmt_year_week,
    is_between_dates,
    total_days_diff_workflow,
    values_by_week,
)
from tests.mocks import config


@fixture
def mock_config(monkeypatch):
    """Mock configuration."""
    monkeypatch.setattr(utils, "config", config)
    yield config
    config.reset()


def test_get_fmt_year_week():
    """Testing get_fmt_year_week."""
    test_cases = [
        (
            """should add a 0 if single digit week.""",
            datetime(year=2000, month=1, day=3),
            "2000_01",
        ),
        (
            """should return double digit week if double digit week.""",
            datetime(year=2000, month=3, day=6),
            "2000_10",
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case
        assert get_fmt_year_week(input_case) == expected, description


def test_total_days_diff():
    """Testing total_days_diff function."""
    test_cases = [
        (
            """should return the total days between dates
            between two dates rounded to 1 decimal place.""",
            (
                datetime(year=2000, month=1, day=3),
                datetime(year=2000, month=1, day=9, hour=12, minute=0, second=0),
            ),
            6.5,
        ),
        (
            """should return 0 if the difference is less
            than the setup config expected cycle time hours.""",
            (
                datetime(year=2000, month=1, day=3),
                datetime(year=2000, month=1, day=3, second=1),
            ),
            0,
        ),
    ]
    for test_case in test_cases:
        description, input_case, expected = test_case
        assert total_days_diff_workflow(*input_case) == expected, description


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


def test_is_between_dates():
    """Test is_between_dates function."""
    cases = [
        {
            "check": datetime(year=2000, month=2, day=1),
            "first": datetime(year=2000, month=1, day=1),
            "second": datetime(year=2000, month=3, day=1),
            "expected": True,
        },
        {
            "check": datetime(year=2000, month=2, day=1),
            "first": datetime(year=2000, month=1, day=1),
            "second": None,
            "expected": True,
        },
        {
            "check": datetime(year=2000, month=1, day=1),
            "first": datetime(year=2000, month=2, day=1),
            "second": datetime(year=2000, month=3, day=1),
            "expected": False,
        },
        {
            "check": datetime(year=2000, month=1, day=1),
            "first": datetime(year=2000, month=2, day=1),
            "second": None,
            "expected": False,
        },
        {
            "check": datetime(year=2000, month=1, day=1),
            "first": datetime(year=2000, month=1, day=1),
            "second": datetime(year=2000, month=1, day=1),
            "expected": True,
        },
    ]

    for case in cases:
        actual = is_between_dates(case["check"], case["first"], case["second"])
        expected = case["expected"]
        assert actual == expected


def test_is_between_dates_error():
    """Test is_between_dates function error condition."""
    with raises(ValueError) as err:
        is_between_dates(
            datetime.now(),
            datetime(year=2000, month=1, day=2),
            datetime(year=2000, month=1, day=1),
        )
    assert str(err.value) == "first_date must not be after second_date"
