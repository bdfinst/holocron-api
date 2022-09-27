"""Security middlewares."""
import logging
from typing import Callable, List, Optional, Union

from flask import request

# Security Settings that are configurable
# The default rate limits provided to the rate limiter
DEFAULT_LIMITS: Optional[List[Union[str, Callable[[], str]]]] = ["300/day", "50/hour"]
# The max input characters the user can use for naming
# their items (example valuestream, organization, team name)
# that they create in the database
MAX_INPUT_CHAR_LEN = 50
# The regex for all the valid characters the user can use for
# string user input (example valuestream, organization, team name)
VALID_NAME_CHARS = "^[a-zA-Z0-9][ a-zA-Z0-9_-]*[a-zA-Z0-9]$"

# All the possible error message for the app related to security
METHOD_NOT_ALLOWED_MSG = "METHOD NOT ALLOWED"
MALFORMED_REQ_PARAMS_MSG = "MALFORMED_PARAMS IN REQUEST"
INVALID_CHARS_IN_BODY = "INVALID CHARACTERS DETECTED IN REQUEST BODY"
SQL_INJECTION = "POSSIBLE SQL INJECTION ATTACK"


def log_security_event(event_description: str):
    """Log security critical event."""
    msg = f"{request.remote_addr} - {request.path} - {event_description}"
    logging.critical(msg)


def get_sanitized_id(id_: str) -> int:
    """Get the id from a user id to query for database."""
    try:
        return int(id_)
    except Exception as err:
        log_security_event(SQL_INJECTION)
        raise err


def on_unexpected_http_methods(_):
    """Log on unexpected HTTP methods or commands."""
    log_security_event(METHOD_NOT_ALLOWED_MSG)
    return "Method Not Allowed", 405
