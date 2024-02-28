"""Pagination utilities."""

import re
from typing import Dict, Optional, Tuple

from app.security import get_sanitized_id


def get_limit_offset_page(params: Dict[str, str]) -> Tuple[int, int, int]:
    """Get the limit, offset, and page from the request parameters."""
    limit = min(get_sanitized_id(params.get("per_page", "100")), 100)
    if limit <= 0:
        limit = 100
    page = get_sanitized_id(params.get("page", "1"))
    if page <= 0:
        page = 1
    offset = (page - 1) * limit
    return limit, offset, page


def construct_next_page_url(
    url: str, limit: int, offset: int, page: int, count: int
) -> Optional[str]:
    """Construct the next page url."""
    if offset + limit >= count:
        return None
    page += 1
    expression = re.compile(r"([?&])page=\d+")
    if re.search(expression, url) is not None:
        return re.sub(expression, f"\\1page={page}", url)
    if "?" in url:
        return f"{url}&page={page}"
    return f"{url}?page={page}"
