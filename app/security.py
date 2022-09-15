"""Security middlewares."""
import logging

from flask import request

# All the possible error message for the app
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
