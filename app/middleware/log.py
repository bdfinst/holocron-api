"""Request logging middleware."""

import logging

from flask import request

from app import config


def log_request() -> None:
    """Log request info."""
    logging.info(f"{request.headers[config.REQUEST_IP_HEADER]} - {request.path}")
    for header in request.headers.keys():
        logging.info(f"{header}={request.headers[header]}")
