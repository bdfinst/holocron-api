"""Security middlewares."""
import logging

from flask import request

# All the possible error message for the app
METHOD_NOT_ALLOWED_MSG = "METHOD NOT ALLOWED"
MALFORMED_REQ_PARAMS_MSG = "MALFORMED_PARAMS IN REQUEST"


def log_security_event(event_description: str):
    """Log security critical event."""
    msg = f"{request.remote_addr} - {request.path} - {event_description}"
    logging.critical(msg)


def on_unexpected_http_methods(_):
    """Log on unexpected HTTP methods or commands."""
    log_security_event(METHOD_NOT_ALLOWED_MSG)
    return "Method Not Allowed", 405
