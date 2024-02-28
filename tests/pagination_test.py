"""Pagination tests."""

from app.utils.pagination import construct_next_page_url, get_limit_offset_page


def test_get_limit_offset_page():
    """Test get_limit_offset_page function."""
    cases = [
        {"input": {"per_page": 10, "page": 5}, "limit": 10, "offset": 40, "page": 5},
        {"input": {"per_page": 10}, "limit": 10, "offset": 0, "page": 1},
        {"input": {"page": 5}, "limit": 100, "offset": 400, "page": 5},
        {
            "input": {"per_page": 1000, "page": 5},
            "limit": 100,
            "offset": 400,
            "page": 5,
        },
        {"input": {"per_page": -5}, "limit": 100, "offset": 0, "page": 1},
        {"input": {"page": 0}, "limit": 100, "offset": 0, "page": 1},
    ]

    for case in cases:
        limit, offset, page = get_limit_offset_page(case["input"])
        assert limit == case["limit"]
        assert offset == case["offset"]
        assert page == case["page"]


def test_construct_next_page_url():
    """Test construct_next_page_url function."""
    cases = [
        {
            "url": "myurl?per_page=5&page=2",
            "limit": 5,
            "offset": 5,
            "page": 2,
            "count": 15,
            "output": "myurl?per_page=5&page=3",
        },
        {
            "url": "myurl?page=2&per_page=5",
            "limit": 5,
            "offset": 5,
            "page": 2,
            "count": 15,
            "output": "myurl?page=3&per_page=5",
        },
        {
            "url": "myurl",
            "limit": 100,
            "offset": 0,
            "page": 1,
            "count": 200,
            "output": "myurl?page=2",
        },
        {
            "url": "myurl?per_page=5",
            "limit": 5,
            "offset": 0,
            "page": 1,
            "count": 100,
            "output": "myurl?per_page=5&page=2",
        },
        {
            "url": "myurl",
            "limit": 100,
            "offset": 0,
            "page": 1,
            "count": 50,
            "output": None,
        },
        {
            "url": "myurl?page=2",
            "limit": 100,
            "offset": 100,
            "page": 2,
            "count": 200,
            "output": None,
        },
    ]

    for case in cases:
        assert (
            construct_next_page_url(
                case["url"], case["limit"], case["offset"], case["page"], case["count"]
            )
            == case["output"]
        )
