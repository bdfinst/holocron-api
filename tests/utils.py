"""Test utilities."""


def first_argument(mock):
    """Return the first argument to a mocked function call."""
    return mock.call_args.args[0]
