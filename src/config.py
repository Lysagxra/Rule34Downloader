"""Configuration module for managing constants and settings used across the project.

These configurations aim to improve modularity and readability by consolidating settings
into a single location.
"""

from aiohttp import ClientTimeout

# ============================
# Paths and Files
# ============================
DOWNLOAD_FOLDER = "Downloads"  # The folder where downloaded files will be stored.
URLS_FILE = "URLs.txt"         # The file containing the list of URLs to process.

# ============================
# Media Configuration
# ============================
MAX_IMAGES_PER_PAGE = 42                     # Maximum number of images per page.
PICS_EXTENSIONS = [".jpeg", ".png", ".gif"]  # Valid image file extensions for pictures.
EXTENSIONS_WHITELIST = [".mp4", ".gif"]      # Extensions allowed for media download
                                             # (videos & gifs).

# Directory names for specific media types
PICS_DIR = "pics"       # Directory for storing image files.
VIDEOS_DIR = "videos"   # Directory for storing video files.
GIFS_DIR = "gifs"       # Directory for storing GIF files.

# Mapping of file extensions to their respective directories
EXTENSIONS_TO_DIR = {
    (".jpg", ".jpeg", ".png"): PICS_DIR,
    (".mp4", ".mkv", ".mov"): VIDEOS_DIR,
    (".gif", ".webp"): GIFS_DIR,
}

# ============================
# Download Settings
# ============================
# Constants for file sizes, expressed in bytes.
KB = 1024
MB = 1024 * KB
CHUNK_SIZE = 64 * KB    # Default chunk size for downloads (in bytes).
MAX_FILE_SIZE = 5 * MB  # Maximum file size for downloads (in bytes).

# ============================
# HTTP / Network Configuration
# ============================
HTTP_STATUS_OK = 200  # HTTP status code for successful responses.

# Timeout settings for HTTP requests
TIMEOUT = ClientTimeout(
    total=60,         # Total request timeout (in seconds)
    connect=10,       # Timeout for establishing the connection (in seconds)
    sock_read=30,     # Timeout for reading a chunk of data (in seconds)
    sock_connect=10,  # Timeout for socket connection (in seconds)
)

# Default headers used for HTTP requests
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"
    ),
    "Connection": "keep-alive",
}
