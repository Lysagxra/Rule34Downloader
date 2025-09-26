"""General utilities module.

This module provides utilities for fetching web pages, managing directories, and
clearing the terminal screen. It includes functions to handle common tasks such as
sending HTTP requests, parsing HTML, creating download directories, and clearing the
terminal, making it reusable across projects.
"""

import logging
import os
import sys

import requests
from bs4 import BeautifulSoup

from .config import HEADERS
from .url_utils import extract_base_url


def get_last_page_url(soup: BeautifulSoup, url: str) -> tuple[BeautifulSoup, str]:
    """Extract the URL of the last page from the given soup object."""
    base_url = extract_base_url(url)

    last_page = soup.find("a", {"href": True, "alt": "last page"})
    if last_page is not None:
        last_page_query = last_page["href"]
        last_page_url = base_url + last_page_query
        return soup, last_page_url

    # If the last page doesn't exist, there is only one page available
    return soup, url


def fetch_page(url: str, *, get_last_page: bool = False) -> BeautifulSoup:
    """Fetch the HTML content of a page and optionally extracts the last page URL."""
    session = requests.Session()

    try:
        response = session.get(url, headers=HEADERS, timeout=(15, 15))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as req_err:
        log_message = f"Error fetching the page {url}: {req_err}"
        logging.exception(log_message)
        sys.exit(1)

    if get_last_page:
        return get_last_page_url(soup, url)

    return soup


def clear_terminal() -> None:
    """Clear the terminal screen based on the operating system."""
    commands = {
        "nt": "cls",       # Windows
        "posix": "clear",  # macOS and Linux
    }

    command = commands.get(os.name)
    if command:
        os.system(command)  # noqa: S605
