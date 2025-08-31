"""Module that provides utility functions for file input and output operations.

It includes methods to read the contents of a file and to write content to a file, with
optional support for clearing the file.
"""

import os
import shutil
from pathlib import Path

from .config import EXTENSIONS_TO_DIR, GIFS_DIR, PICS_DIR, VIDEOS_DIR


def read_file(filename: str) -> list[str]:
    """Read the contents of a file and returns a list of its lines."""
    with Path(filename).open("r", encoding="utf-8") as file:
        return file.read().splitlines()


def write_file(filename: str, content: str = "") -> None:
    """Write content to a specified file.

    If content is not provided, the file is cleared.
    """
    with Path(filename).open("w", encoding="utf-8") as file:
        file.write(content)


def move_files(source_dir: str) -> None:
    """Move files from the source directory to designated subdirectories."""
    for target_dir in [PICS_DIR, VIDEOS_DIR, GIFS_DIR]:
        target_dir_path = Path(source_dir) / target_dir
        target_dir_path.mkdir(parents=True, exist_ok=True)

    for filename in os.listdir(source_dir):
        source_path = Path(source_dir) / filename

        if Path(source_path).is_file():
            file_extension = Path(filename).suffix.lower()
            target_dir = None

            for extensions, dir_name in EXTENSIONS_TO_DIR.items():
                if file_extension in extensions:
                    target_dir = dir_name
                    break

            if target_dir:
                target_path = Path(source_dir) / target_dir / filename
                shutil.move(source_path, target_path)
