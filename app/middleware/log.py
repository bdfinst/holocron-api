"""Request logging middleware."""
import logging

from flask import request


def log_request():
    """Log request info."""
    logging.info(request.headers)
    logging.info(f"{request.remote_addr} - {request.path}")
