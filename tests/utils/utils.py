"""Test utilities."""

from functools import wraps
from typing import Callable


def first_argument(mock):
    """Return the first argument to a mocked function call."""
    return mock.call_args.args[0]


def second_argument(mock):
    """Return the first argument to a mocked function call."""
    return mock.call_args.args[1]
