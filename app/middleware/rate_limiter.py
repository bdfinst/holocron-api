"""Rate limiter."""

from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.config import REQUEST_IP_HEADER
from app.security import DEFAULT_LIMITS, RATE_LIMITING_IP_WHITELIST

limiter = Limiter(
    key_func=get_remote_address, default_limits=DEFAULT_LIMITS, storage_uri="memory://"
)


@limiter.request_filter
def ip_whitelist():
    """Check if request came from whitelisted IP."""
    return request.headers[REQUEST_IP_HEADER] in RATE_LIMITING_IP_WHITELIST
