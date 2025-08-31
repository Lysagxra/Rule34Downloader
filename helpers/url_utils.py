"""Module that provides utility functions for manipulating URLs.

It includes functionality for extracting base URLs, query parameters, and specific
parameters such as 'pid'. Additionally, it supports updating query parameters in a URL.
"""

from __future__ import annotations

from urllib.parse import ParseResult, parse_qs, unquote, urlencode, urlparse, urlunparse


def parse_url(url: str) -> ParseResult:
    """Parse a URL into its components after decoding."""
    return urlparse(unquote(url))


def unparse_url(parsed_url: ParseResult) -> str:
    """Reconstruct a URL from its parsed components."""
    return urlunparse(parsed_url)


def extract_base_url(url: str) -> str:
    """Extract the base URL (scheme, netloc, and path) from a full URL."""
    parsed_url = urlparse(url)
    return urlunparse(parsed_url._replace(query="", fragment=""))


def extract_query_params(url: str) -> dict:
    """Extract query parameters from a URL as a dictionary."""
    decoded_url = unquote(url)
    parsed_url = urlparse(decoded_url)
    return parse_qs(parsed_url.query)


def extract_or_update_pid(url: str, updated_pid: str | None = None) -> int | str:
    """Extract the 'pid' parameter from a URL or updates it with a new value."""
    parsed_url = parse_url(url)
    query_params = parse_qs(parsed_url.query)

    if updated_pid:
        query_params["pid"] = [updated_pid]
        updated_query = urlencode(query_params, doseq=True)
        updated_url = parsed_url._replace(query=updated_query)
        return urlunparse(updated_url)

    pid = query_params.get("pid", [None])[0]
    return int(pid) if pid and pid.isdigit() else 0
