"""Pagination utilities."""

import re
from dataclasses import dataclass
from typing import Dict

from flask import Response

from app.security import get_sanitized_id


@dataclass
class PaginationInfo:
    """Data container for pagination information."""

    limit: int
    offset: int
    page: int
    count: int


def get_pagination_info(req_params: Dict[str, str], count: int) -> PaginationInfo:
    """Get the limit, offset, and page from the request parameters."""
    limit = min(get_sanitized_id(req_params.get("per_page", "100")), 1000)
    if limit <= 0:
        limit = 100
    page = get_sanitized_id(req_params.get("page", "1"))
    if page <= 0:
        page = 1
    offset = (page - 1) * limit
    return PaginationInfo(limit, offset, page, count)


def set_pagination_header(
    response: Response, url: str, page_info: PaginationInfo
) -> Response:
    """Construct the next page url."""
    if page_info.offset + page_info.limit >= page_info.count:
        response.headers["x-next-page"] = "None"
        return response
    page_info.page += 1
    expression = re.compile(r"([?&])page=\d+")
    if re.search(expression, url) is not None:
        response.headers["x-next-page"] = re.sub(
            expression, f"\\1page={page_info.page}", url
        )
    elif "?" in url:
        response.headers["x-next-page"] = f"{url}&page={page_info.page}"
    else:
        response.headers["x-next-page"] = f"{url}?page={page_info.page}"
    return response
