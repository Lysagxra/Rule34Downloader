"""Module that handles download links, URL validation, and generating download URLs.

This module provides functions for validating, constructing, and retrieving
download links for media content, with support for retries and alternative
formats. It also supports paginated content and image/sample link construction.
"""

import asyncio
import logging
import random
import sys
from pathlib import Path

from aiohttp import ClientConnectionError, ClientSession

from helpers.url_utils import (
    extract_or_update_pid,
    extract_query_params,
    parse_url,
    unparse_url,
)

from .config import HEADERS, HTTP_STATUS_OK, MAX_IMAGES_PER_PAGE, PICS_EXTENSIONS


async def validate_url(session: ClientSession, url: str) -> bool:
    """Validate if a URL is reachable by sending an asynchronous HEAD request."""
    try:
        async with session.head(url, headers=HEADERS) as response:
            return response.status == HTTP_STATUS_OK

    except ClientConnectionError as req_err:
        log_message = f"Connection error with {url}: {req_err}"
        logging.exception(log_message)
        return False


def get_tag_name(url: str) -> str:
    """Extract the tag name from a URL by decoding and splitting it."""
    try:
        query_params = extract_query_params(url)
        return query_params.get("tags", [None])[0]

    except ValueError as val_err:
        log_message = f"Error extracting name from {url}: {val_err}"
        logging.exception(log_message)
        sys.exit(1)


def generate_page_urls(url: str, last_page_url: str) -> list[str]:
    """Generate a list of page URLs for paginated content."""
    if last_page_url == url:
        return [url]

    current_page_pid = extract_or_update_pid(url)
    last_page_pid = extract_or_update_pid(last_page_url)
    total_pages = (
        last_page_pid - 1 + MAX_IMAGES_PER_PAGE - current_page_pid
    ) // MAX_IMAGES_PER_PAGE

    page_urls = [url]
    for current_page in range(1, total_pages + 1):
        next_pid = current_page_pid + current_page * MAX_IMAGES_PER_PAGE
        page_url = extract_or_update_pid(url, updated_pid=next_pid)
        page_urls.append(page_url)

    return page_urls


def construct_sample_download_link(download_link: str) -> str:
    """Convert an image download link to a sample download link."""
    parsed_url = parse_url(download_link)
    url_path = parsed_url.path
    url_path = url_path.replace("images", "samples")

    base_name = Path(url_path).name
    filename = Path(base_name).stem
    new_base_name = f"sample_{filename}.jpg"

    new_url_path = str(Path(url_path).parent / new_base_name)
    sample_download_link = parsed_url._replace(path=new_url_path)
    return unparse_url(sample_download_link)


async def get_alternative_download_link(
    session: ClientSession,
    download_link: str,
    retries: int = 5,
) -> str:
    """Attempt to retrieve an alternative download link if the primary fail."""
    for attempt in range(retries):
        for extension in PICS_EXTENSIONS:
            alt_download_link = download_link.replace(".jpg", extension)
            if await validate_url(session, alt_download_link):
                return alt_download_link

        if attempt < retries - 1:
            delay = 2 ** (attempt + 1) + random.uniform(0, 1)  # noqa: S311
            await asyncio.sleep(delay)

    log_message = f"Error extracting real download link for {download_link}"
    logging.warning(log_message)
    return download_link


async def construct_download_link(
    session: ClientSession,
    preview_link: str,
    preview_info: str,
) -> str:
    """Convert a preview image link into its corresponding download link."""
    download_link = preview_link.replace("thumbnails", "images").replace(
        "thumbnail_", "",
    )

    if "video " in preview_info:
        return download_link.replace("wimg.", "webm.").replace(".jpg", ".mp4")

    if await validate_url(session, download_link):
        return download_link

    return await get_alternative_download_link(session, download_link)


async def get_download_links(preview_images: list[str]) -> list[str]:
    """Generate a list of download links from a list of preview image elements."""
    async with ClientSession() as session:
        tasks = [
            construct_download_link(session, image["src"], image["title"])
            for image in preview_images
        ]
        return await asyncio.gather(*tasks)
