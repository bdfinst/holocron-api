"""Text validation middleware."""
import re
from typing import Optional, Tuple

from flask import request

reg_exp = re.compile("[\\x20-\\x7E]+")


def validate_text() -> Optional[Tuple[str, int]]:
    """Vaidate text only has acceptable characters."""
    if request.mimetype == "application/json":
        body = str(request.json)
        if reg_exp.fullmatch(body) is None:
            return "Invalid characters detected in request body", 400
    return None
