"""Configuration module for managing constants and settings used across the project.

These configurations aim to improve modularity and readability by consolidating settings
into a single location.
"""

from aiohttp import ClientTimeout

URLS_FILE = "URLs.txt"
DOWNLOAD_FOLDER = "Downloads"

MAX_IMAGES_PER_PAGE = 42
PICS_EXTENSIONS = [".jpeg", ".png", ".gif"]
EXTENSIONS_WHITELIST = [".mp4", ".gif"]

PICS_DIR = "pics"
VIDEOS_DIR = "videos"
GIFS_DIR = "gifs"
EXTENSIONS_TO_DIR = {
    (".jpg", ".jpeg", ".png"): PICS_DIR,
    (".mp4", ".mkv", ".mov"): VIDEOS_DIR,
    (".gif", ".webp"): GIFS_DIR,
}

KB = 1024
MB = 1024 * KB
CHUNK_SIZE = 64 * KB
MAX_FILE_SIZE = 5 * MB

HTTP_STATUS_OK = 200
TIMEOUT = ClientTimeout(
    total=60,         # Total request timeout (in seconds)
    connect=10,       # Timeout for establishing the connection
    sock_read=30,     # Timeout for reading a chunk of data
    sock_connect=10,  # Timeout for socket connection
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"
    ),
    "Connection": "keep-alive",
}
