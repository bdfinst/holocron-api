"""Text validation middleware."""

import re
from typing import Optional, Tuple

from flask import request

from app.security import INVALID_CHARS_IN_BODY, log_security_event

reg_exp = re.compile("[\\x20-\\x7E]+")


def validate_text() -> Optional[Tuple[str, int]]:
    """Vaidate text only has acceptable characters."""
    if request.mimetype == "application/json":
        body = str(request.json)
        if reg_exp.fullmatch(body) is None:
            log_security_event(INVALID_CHARS_IN_BODY)
            return "Invalid characters detected in request body", 400
    return None
