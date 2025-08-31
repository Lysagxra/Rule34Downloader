# Rule34 Downloader

> A Python-based tool for downloading hanime from rule34.xxx. This tool reads a list of URLs from a file and processes the downloads accordingly.

![Demo]()

## Features

- Downloads multiple files concurrently.
- Supports [batch downloading](https://github.com/Lysagxra/Rule34Downloader/tree/main?tab=readme-ov-file#batch-download) via a list of URLs.
- Tracks download progress with a progress bar.
- Automatically creates a directory structure for organized storage.

## Dependencies

- Python 3
- `aiofiles` - async file handling for non-blocking file I/O operations
- `aiohttp` - async HTTP client/server for non-blocking web requests
- `BeautifulSoup` (bs4) - for HTML parsing
- `requests` - for HTTP requests
- `rich` - for progress display in the terminal

## Directory Structure

```
project-root/
├── helpers/
│ ├── config.py                # Manages constants and settings used across the project
│ ├── download_utils.py        # Utilities for managing the download process
│ ├── file_utils.py            # Utilities for managing file operations
│ ├── general_utils.py         # Miscellaneous utility functions
│ ├── progress_utils           # Utilities for displaying and managing progress
│ ├── rule34_utils             # Utilities for interacting with Rule34
│ └── url_utils                # Utilities for handling URL manipulation
├── downloader.py              # Module for initiating downloads from specified rule34.xxx
├── main.py                    # Main script to run the downloader
└── URLs.txt                   # Text file listing album URLs to be downloaded
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Lysagxra/Rule34Downloader.git
```

2. Navigate to the project directory:

```bash
cd Rule34Downloader
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Batch Download

To batch download from multiple URLs, you can use the `main.py` script. This script reads URLs from a file named `URLs.txt` and downloads each one using the album downloader.

### Usage

1. Create a file named `URLs.txt` in the root of your project, listing each URL on a new line.

- Example of `URLs.txt`:

```
https://rule34.xxx/index.php?page=post&s=list&tags=gumi_arts&pid=84
https://rule34.xxx/index.php?page=post&s=list&tags=wodstudio&pid=0
https://rule34.xxx/index.php?page=post&s=list&tags=jennieart02
```

- Ensure that each URL is on its own line without any extra spaces.
- You can add as many URLs as you need, following the same format.

2. Run the batch download script:

```
python3 main.py
```

3. The downloaded files will be saved in the `Downloads` directory.

## Logging

The application logs any issues encountered during the download process.
