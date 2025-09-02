"""Module for handling large file downloads, saving with progress, and managing retries.

This module provides asynchronous functions to download large files with progress
tracking, handle sample file downloads, and write the content in chunks to avoid
timeouts. It also includes automatic retries for failed downloads.
"""

from __future__ import annotations

import asyncio
import random
from pathlib import Path

import aiofiles
from aiohttp import ClientResponse, ClientSession

from .config import CHUNK_SIZE, EXTENSIONS_WHITELIST, HEADERS, MAX_FILE_SIZE, TIMEOUT
from .rule34_utils import construct_sample_download_link


async def handle_large_file(download_info: tuple, task_info: tuple) -> bool:
    """Handle the download of large files by converting them to sample files."""
    file_size, download_link, download_path = download_info
    job_progress, task = task_info
    not_in_whitelist = not any(
        extension in download_link for extension in EXTENSIONS_WHITELIST
    )

    if file_size > MAX_FILE_SIZE and not_in_whitelist:
        sample_download_link = construct_sample_download_link(download_link)
        file_name = sample_download_link.split("/")[-1].split("?")[0]
        final_path = Path(download_path) / file_name

        async with (
            ClientSession(timeout=TIMEOUT) as session,
            session.get(sample_download_link, headers=HEADERS) as response,
        ):
            await write_file_chunks(response, final_path)

        job_progress.advance(task)
        return True

    return False


async def write_file_chunks(
    response: ClientResponse,
    final_path: str,
    chunk_size: int | None = None,
) -> None:
    """Write the content of a response to a file in chunks."""
    async with aiofiles.open(final_path, "wb") as file:
        chunk_iterator = (
            response.content.iter_chunked(chunk_size)
            if chunk_size
            else response.content.iter_any()
        )
        async for chunk in chunk_iterator:
            await file.write(chunk)


async def save_file_with_progress(
    session: ClientSession,
    download_link: str,
    download_path: str,
    task_info: tuple,
    retries: int = 5,
) -> None:
    """Download a file with progress tracking and retries on failure."""
    job_progress, task = task_info
    file_name = download_link.split("/")[-1].split("?")[0]
    final_path = Path(download_path) / file_name

    for attempt in range(retries):
        async with session.get(download_link, headers=HEADERS) as response:
            try:
                file_size = int(response.headers.get("Content-Length", -1))
                file_handled = await handle_large_file(
                    (file_size, download_link, download_path),
                    (job_progress, task),
                )
                if not file_handled:
                    await write_file_chunks(response, final_path, chunk_size=CHUNK_SIZE)
                    job_progress.advance(task)

            except asyncio.TimeoutError:
                if attempt < retries - 1:
                    delay = 2 ** (attempt + 1) + random.uniform(1, 3)  # noqa: S311
                    await asyncio.sleep(delay)

            else:
                return
