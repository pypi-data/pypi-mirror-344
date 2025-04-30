import pathlib

from .download import download_archive
from .extract import extract_archive


def uncloud(
    url: str,
    download_to: str | pathlib.Path | None = None,
    filename: str | None = None,
    md5: str | None = None,
    extract: bool = True,
    extract_to: str | pathlib.Path | None = None,
    remove: bool = False,
    verbose: bool = False,
) -> None:
    """
    Download (and extract) a public archive file from popular cloud storage services such as Dropbox, Google Drive, and OneDrive.

    Supported cloud storage services for downloading:
    - Dropbox
    - Google Drive
    - OneDrive

    Supported archive formats for extraction:
    - tar
    - ZIP

    Args:
        url (str): The share link URL of the archive file to download.
        download_to (str | pathlib.Path | None): The path to the directory where the archive file will be downloaded. If None, it will be the current working directory.
        filename (str | None): The filename of the archive file to download. If None, it will be inferred.
        md5 (str | None): The MD5 checksum of the archive file for integrity verification. If None, the integrity check is skipped.
        extract (bool): If True, extract the archive file after downloading.
        extract_to (str | pathlib.Path | None): The path to the directory where the archive file will be extracted. If None, it will default to `download_to`.
        remove (bool): If True, remove the archive file after extraction.
        verbose (bool): If True, enable verbosity.
    """
    if download_to is None:
        download_to = "."
    file = download_archive(url, download_to, filename, md5, verbose)
    if extract:
        if extract_to is None:
            extract_to = download_to
        extract_archive(file, extract_to, remove, verbose)


def download_and_extract_archive(
    url: str,
    download_root: str | pathlib.Path,
    extract_root: str | pathlib.Path | None = None,
    filename: str | None = None,
    md5: str | None = None,
    remove_finished: bool = False,
) -> None:
    """
    Download and extract a public archive from popular cloud storage services such as Dropbox, Google Drive, and OneDrive.

    Supported cloud storage services for downloading:
    - Dropbox
    - Google Drive
    - OneDrive

    Supported archive formats for extraction:
    - tar
    - ZIP

    Args:
        url (str): The share link URL of the archive to download.
        download_root (str | pathlib.Path): The path to the directory where the archive will be downloaded.
        extract_root (str | pathlib.Path | None): The path to the directory where the archive will be extracted. If None, it will default to `download_root`.
        filename (str | None): The filename of the archive to download. If None, it will be inferred.
        md5 (str | None): The MD5 checksum of the archive for integrity verification. If None, the integrity check is skipped.
        remove_finished (bool): If True, remove the archive after extraction.
    """
    uncloud(url, download_root, filename, md5, extract_root, remove_finished)
