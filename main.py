"""Main module of the project.

This module provides functionality for reading URLs from a file, processing
them to download media content, and clearing the file after the process is
complete.

Usage:
    Ensure that a file named 'URLs.txt' is present in the same directory as
    this script. The file should contain a list of URLs, one per line. When
    executed, the script will:
        1. Read the URLs from 'URLs.txt'.
        2. Process each URL for downloading media content.
        3. Clear the contents of 'URLs.txt' after all URLs have been processed.
"""

import asyncio

from downloader import process_tag_download
from helpers.config import URLS_FILE
from helpers.file_utils import read_file, write_file
from helpers.general_utils import clear_terminal


async def process_urls(urls: list[str]) -> None:
    """Validate and downloads items for a list of URLs."""
    for url in urls:
        await process_tag_download(url)


async def main() -> None:
    """Run the script."""
    # Clear the terminal
    clear_terminal()

    # Read and process URLs, ignoring empty lines
    urls = [url.strip() for url in read_file(URLS_FILE) if url.strip()]
    await process_urls(urls)

    # Clear URLs file
    write_file(URLS_FILE)


if __name__ == "__main__":
    asyncio.run(main())
