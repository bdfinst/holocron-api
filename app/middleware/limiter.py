"""Rate limiter."""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.security import DEFAULT_LIMITS

limiter = Limiter(
    key_func=get_remote_address, default_limits=DEFAULT_LIMITS, storage_uri="memory://"
)
