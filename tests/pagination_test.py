"""Pagination tests."""

from flask import Response

from app.utils.pagination import (
    PaginationInfo,
    get_pagination_info,
    set_pagination_header,
)


def test_get_limit_offset_page():
    """Test get_limit_offset_page function."""
    cases = [
        {"input": {"per_page": 10, "page": 5}, "limit": 10, "offset": 40, "page": 5},
        {"input": {"per_page": 10}, "limit": 10, "offset": 0, "page": 1},
        {"input": {"page": 5}, "limit": 100, "offset": 400, "page": 5},
        {
            "input": {"per_page": 10000, "page": 5},
            "limit": 1000,
            "offset": 4000,
            "page": 5,
        },
        {"input": {"per_page": -5}, "limit": 100, "offset": 0, "page": 1},
        {"input": {"page": 0}, "limit": 100, "offset": 0, "page": 1},
    ]

    for case in cases:
        page_info = get_pagination_info(case["input"], 0)
        assert page_info.limit == case["limit"]
        assert page_info.offset == case["offset"]
        assert page_info.page == case["page"]
        assert page_info.count == 0


def test_construct_next_page_url():
    """Test construct_next_page_url function."""
    response = Response()
    cases = [
        {
            "url": "myurl?per_page=5&page=2",
            "page_info": PaginationInfo(limit=5, offset=5, page=2, count=15),
            "output": "myurl?per_page=5&page=3",
        },
        {
            "url": "myurl?page=2&per_page=5",
            "page_info": PaginationInfo(limit=5, offset=5, page=2, count=15),
            "output": "myurl?page=3&per_page=5",
        },
        {
            "url": "myurl",
            "page_info": PaginationInfo(limit=100, offset=0, page=1, count=200),
            "output": "myurl?page=2",
        },
        {
            "url": "myurl?per_page=5",
            "page_info": PaginationInfo(limit=5, offset=0, page=1, count=100),
            "output": "myurl?per_page=5&page=2",
        },
        {
            "url": "myurl",
            "page_info": PaginationInfo(limit=100, offset=0, page=1, count=50),
            "output": "None",
        },
        {
            "url": "myurl?page=2",
            "page_info": PaginationInfo(limit=100, offset=100, page=2, count=200),
            "output": "None",
        },
    ]

    for case in cases:
        assert (
            set_pagination_header(response, case["url"], case["page_info"]).headers[
                "x-next-page"
            ]
            == case["output"]
        )
