"""Module that provides functionality to download images and videos from a given URL.

It uses asynchronous HTTP requests with `aiohttp` for efficient file downloading, and
`rich` for progress bar visualization.

Usage:
    To run the script, execute with a URL as an argument:
    python script.py <url>
"""

import asyncio
import random
import sys

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from rich.live import Live
from rich.progress import Progress

from helpers.config import TIMEOUT
from helpers.download_utils import save_file_with_progress
from helpers.file_utils import move_files
from helpers.general_utils import clear_terminal, create_download_directory, fetch_page
from helpers.progress_utils import create_progress_bar, create_progress_table
from helpers.rule34_utils import generate_page_urls, get_download_links, get_tag_name


async def download_video_items(
    video_download_links: list[str], download_path: str, task_info: tuple,
) -> None:
    """Download video files with progress tracking."""
    async with ClientSession(timeout=TIMEOUT) as session:
        for video_download_link in video_download_links:
            await save_file_with_progress(
                session,
                video_download_link,
                download_path,
                task_info,
            )


async def download_items(
    download_links: list[str],
    video_download_links: list[str],
    download_path: str,
    task_info: tuple,
) -> None:
    """Download multiple video files with progress tracking."""
    job_progress, task_title = task_info
    num_items = len([*download_links, *video_download_links])
    task = job_progress.add_task(f"[cyan]{task_title}", total=num_items)

    async with ClientSession(timeout=TIMEOUT) as session:
        tasks = [
            save_file_with_progress(
                session,
                download_link,
                download_path,
                (job_progress, task),
            )
            for download_link in download_links
            if download_link
        ]
        await asyncio.gather(*tasks)

        await asyncio.sleep(random.uniform(3, 5))  # noqa: S311
        await download_video_items(
            video_download_links,
            download_path,
            (job_progress, task),
        )

    job_progress.update(task, visible=False)


async def process_and_download_items(
    soup: BeautifulSoup, download_path: str, task_info: tuple,
) -> None:
    """Process and downloads video items and preview images."""

    def pop_video_download_links(download_links: list[str]) -> list[str]:
        """Filter and remove video download links from the list."""
        return [link for link in reversed(download_links) if ".mp4" in link]

    preview_images = soup.find_all(
        "img", {"class": "preview", "src": True, "title": True},
    )
    download_links = await get_download_links(preview_images)
    video_download_links = pop_video_download_links(download_links)
    await download_items(download_links, video_download_links, download_path, task_info)


async def download_pages(
    page_urls: list[str],
    initial_soup: BeautifulSoup,
    download_path: str,
    job_progress: Progress,
) -> None:
    """Download pages and process video items and images."""

    def fetch_page_soup(url: str) -> BeautifulSoup:
        """Fetch and parse page content."""
        return initial_soup if url == page_urls[0] else fetch_page(url)

    num_pages = len(page_urls)
    overall_task = job_progress.add_task("[cyan]Progress", total=num_pages)

    for indx, page_url in enumerate(page_urls):
        task_title = f"Page {indx + 1}/{num_pages}"
        page_soup = fetch_page_soup(page_url)
        await process_and_download_items(
            page_soup, download_path, (job_progress, task_title),
        )
        job_progress.advance(overall_task)
        move_files(download_path)
        await asyncio.sleep(random.uniform(3, 5))  # noqa: S311


async def process_tag_download(url: str) -> None:
    """Process and download items for a given tag from a URL."""
    tag_name = get_tag_name(url)
    download_path = create_download_directory(tag_name)

    initial_soup, last_page_url = fetch_page(url, get_last_page=True)
    page_urls = generate_page_urls(url, last_page_url)

    job_progress = create_progress_bar()
    progress_table = create_progress_table(tag_name, job_progress)

    with Live(progress_table, refresh_per_second=10):
        await download_pages(page_urls, initial_soup, download_path, job_progress)


async def main() -> None:
    """Run the script."""
    clear_terminal()
    url = sys.argv[1]
    await process_tag_download(url)


if __name__ == "__main__":
    asyncio.run(main())
