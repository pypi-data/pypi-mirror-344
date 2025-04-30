import datetime
import hashlib
import pathlib
import re
import subprocess
import urllib
from typing import Any

import requests
from tqdm.auto import tqdm

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# a Chrome user agent on macOS
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"


def compute_md5(file: str | pathlib.Path, chunk_size: int = 1024 * 1024) -> str:
    """
    Compute the MD5 checksum of an archive.

    Args:
        file (str | pathlib.Path): The path to the archive.
        chunk_size (int): The size of the chunks to read from the archive. Default is 1MB.

    Returns:
        str: The MD5 checksum of the archive.
    """
    md5 = hashlib.md5(usedforsecurity=False)
    with open(file, mode="rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()


def _check_md5(file: pathlib.Path, md5: str, **kwargs: Any) -> bool:
    """Check if an archive matches the given MD5 checksum."""
    return md5 == compute_md5(file, **kwargs)


def check_integrity(file: str | pathlib.Path, md5: str | None = None) -> bool:
    """
    Check the integrity of an archive by verifying its MD5 checksum.

    Args:
        file (str | pathlib.Path): The path to the archive.
        md5 (str | None): The expected MD5 checksum of the archive. If None, the integrity check is skipped.

    Returns:
        bool: True if the archive matches the given MD5 checksum, otherwise False.
    """
    file = pathlib.Path(file)

    # check if the archive exists and is a file
    if not file.exists():
        raise FileNotFoundError(f"Archive '{file}' does not exist.")
    if not file.is_file():
        raise ValueError(f"Archive '{file}' is not a file.")

    if md5 is None:
        return True
    return _check_md5(file, md5)


_HOSTNAME_TO_CLOUD_STORAGE_SERVICE = {
    "www.dropbox.com": "Dropbox",
    "drive.google.com": "Google Drive",
    "onedrive.live.com": "OneDrive",
}


def _get_redirect_url(url: str, max_redirects: int = 3) -> str:
    """Get the redirect URL from a URL."""
    initial_url = url

    headers = {"User-Agent": USER_AGENT}

    for _ in range(max_redirects + 1):
        with urllib.request.urlopen(
            urllib.request.Request(url, headers=headers)
        ) as r:
            if r.url == url or r.url is None:
                return url

            url = r.url
    else:
        raise RecursionError(
            f"Request to '{initial_url}' exceeded {max_redirects} redirects. The last redirect points to '{url}'."
        )


def _get_hostname(url: str) -> str:
    """Get the hostname from a URL."""
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.hostname


def _get_filename_from_response(response: requests.Response) -> str | None:
    """Get the filename from the response."""
    content_disposition = urllib.parse.unquote(
        response.headers["Content-Disposition"]
    )

    m = re.search(r'filename="(.*?)"', content_disposition)
    if m:
        filename = m.groups()[0]
        return filename

    return None


def _download(
    url: str,
    to: pathlib.Path,
    filename: str | None = None,
    partial: bool = False,
    chunk_size: int = 10 * 1024 * 1024,
    timeout: int = 30,
    verbose: bool = False,
) -> pathlib.Path:
    """Download a public file from popular cloud storage services using its download link URL."""
    headers = {"User-Agent": USER_AGENT}

    with requests.get(
        url, headers=headers, timeout=timeout, stream=True, verify=True
    ) as r:
        r.raise_for_status()
        filename = filename or _get_filename_from_response(r)

    if filename is None:
        raise ValueError("Failed to infer the filename")

    file = to / filename

    # try:
    #     command = f"curl '{url}' -o '{file}'"

    #     if verbose:
    #         timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
    #         print(f"[{timestamp}] ⬇  {command}")

    #     subprocess.run(command, shell=True, check=True)
    #     return file

    # except subprocess.CalledProcessError as e:

    #     if verbose:
    #         timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
    #         print(f"[{timestamp}] ⬇  curl failed: {e}")

    # except Exception as e:

    #     if verbose:
    #         timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
    #         print(f"[{timestamp}] ⬇  Unexpected error occurred: {e}")

    temp_file = to / f"{filename}.part" if partial else file

    mode = "ab" if partial and temp_file.exists() else "wb"

    resume_from = temp_file.stat().st_size if mode == "ab" else 0

    if resume_from:
        headers.update({"Range": f"bytes={resume_from}-"})

    with requests.get(
        url, headers=headers, timeout=timeout, stream=True, verify=True
    ) as r:
        r.raise_for_status()

        total = int(r.headers.get("content-length", 0)) + resume_from
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        progress_bar = tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            initial=resume_from,
            disable=(not verbose) or (total == 0),
            desc=f"[{timestamp}] ⬇  Downloading the archive '{filename}' using requests",
        )

        with open(temp_file, mode=mode) as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))

        progress_bar.close()

    if partial:
        temp_file.replace(file)

    return file


def _get_download_url_for_dropbox(url) -> str:
    """Get the download link URL for Dropbox."""
    return url.replace("dl=0", "dl=1")


def _download_archive_from_dropbox(
    url: str,
    to: pathlib.Path,
    filename: str | None = None,
    verbose: bool = False,
) -> pathlib.Path:
    """Download a public archive from Dropbox using its share link URL."""
    initial_url = url
    url = _get_download_url_for_dropbox(url)

    if verbose and url != initial_url:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        print(f"[{timestamp}] ▶ Redirected URL from '{initial_url}' to '{url}'")

    return _download(url, to, filename, partial=True, verbose=verbose)


def _get_download_url_for_google_drive(url) -> str:
    """Get the download link URL for Google Drive."""
    parsed_url = urllib.parse.urlparse(url)

    patterns = [
        r"^/uc?id=(.*?)",
        r"^/file/d/(.*?)/(edit|view)$",
    ]
    for pattern in patterns:
        match = re.match(pattern, parsed_url.path)
        if match:
            id = match.groups()[0]
            break

    return f"https://drive.google.com/uc?id={id}"


def _download_archive_from_google_drive(
    url: str,
    to: pathlib.Path,
    filename: str | None = None,
    verbose: bool = False,
) -> pathlib.Path:
    """Download a public archive from Google Drive using its share link URL."""
    initial_url = url
    url = _get_download_url_for_google_drive(url)

    if verbose and url != initial_url:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        print(f"[{timestamp}] ▶ Redirected URL from '{initial_url}' to '{url}'")

    return _download(url, to, filename, partial=True, verbose=verbose)


def _get_download_url_for_one_drive(url, timeout: int = 30_000) -> str:
    """Get the download link URL for Microsoft OneDrive."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError(
            "Playwright is required. Please install it using 'pip install playwright' and install Chromium using `playwright install chromium`"
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            page.goto(url, timeout=timeout)

            # wait until a visible Download button is present
            download_button = page.locator("text=Download").first
            download_button.wait_for(state="visible", timeout=timeout)

            with page.expect_download() as download_info:
                download_button.click()

            download = download_info.value

            # filename = filename or download.suggested_filename
            # file = to / filename
            # download.save_as(str(file))

            # return file

            return download.url
        finally:
            browser.close()


def _download_archive_from_one_drive(
    url: str,
    to: pathlib.Path,
    filename: str | None = None,
    verbose: bool = False,
) -> pathlib.Path:
    """Download a public archive from Microsoft OneDrive using its share link URL."""
    initial_url = url
    url = _get_download_url_for_one_drive(url)

    if verbose and url != initial_url:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        print(f"[{timestamp}] ▶ Redirected URL from '{initial_url}' to '{url}'")

    return _download(url, to, filename, partial=True, verbose=verbose)


def download_archive(
    url: str,
    to: str | pathlib.Path,
    filename: str | None = None,
    md5: str | None = None,
    verbose: bool = False,
) -> pathlib.Path:
    """
    Download a public archive from popular cloud storate services using its share link URL.

    Supported cloud storage services for downloading:
    - Dropbox
    - Google Drive
    - OneDrive

    Args:
        url (str): The share link URL of the archive to download.
        to (str | pathlib.Path): The path to the directory where the archive will be downloaded.
        filename (str | None): The filename of the archive to download. If None, it will be inferred.
        md5 (str | None): The MD5 checksum of the archive to verify its integrity. If None, the integrity check is skipped.
        verbose (bool): If True, enable verbosity.

    Returns:
        pathlib.Path: The path to the downloaded archive.
    """
    initial_url = url
    url = _get_redirect_url(url)

    if verbose and url != initial_url:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        print(f"[{timestamp}] ▶ Redirected URL from '{initial_url}' to '{url}'")

    to = pathlib.Path(to)
    to.mkdir(parents=True, exist_ok=True)

    hostname = _get_hostname(url)

    # check if the URL has a valid hostname
    if hostname not in _HOSTNAME_TO_CLOUD_STORAGE_SERVICE:
        raise ValueError(f"URL '{url}' has an unknown hostname '{hostname}'.")

    if _HOSTNAME_TO_CLOUD_STORAGE_SERVICE[hostname] == "Dropbox":
        file = _download_archive_from_dropbox(url, to, filename, verbose)
    elif _HOSTNAME_TO_CLOUD_STORAGE_SERVICE[hostname] == "Google Drive":
        file = _download_archive_from_google_drive(url, to, filename, verbose)
    elif _HOSTNAME_TO_CLOUD_STORAGE_SERVICE[hostname] == "OneDrive":
        file = _download_archive_from_one_drive(url, to, filename, verbose)

    if not check_integrity(file, md5):
        raise RuntimeError(f"Archive '{file}' not found or corrupted.")

    if verbose:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        print(
            f"[{timestamp}] ⬇  Downloaded the archive '{file}' from '{initial_url}'"
        )

    return file
