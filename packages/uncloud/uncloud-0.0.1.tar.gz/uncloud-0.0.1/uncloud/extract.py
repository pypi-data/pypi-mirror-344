import datetime
import pathlib
import subprocess
import tarfile
import zipfile

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

_EXTENSION_TO_TAR_COMPRESSION: dict[str, str | None] = {
    ".tar": None,
    ".tar.gz": "gz",
    ".tgz": "gz",
    ".tar.bz2": "bz2",
    ".tbz2": "bz2",
    ".tar.xz": "xz",
    ".txz": "xz",
}

_TAR_COMPRESSION_TO_OPTION: dict[str, str] = {
    "gz": "z",
    "bz2": "j",
    "xz": "J",
}

_EXTENSION_TO_ZIP_COMPRESSION: dict[str, int] = {
    ".zip": zipfile.ZIP_STORED,
}


def _get_extension(file: pathlib.Path) -> str:
    """Get the filename extension of a file."""
    return "".join(pathlib.Path(file).suffixes)


def _extract_tar_archive(
    file: pathlib.Path,
    to: pathlib.Path | None = None,
    compression: str | None = None,
    verbose: bool = False,
) -> None:
    """Extract a tar archive."""
    try:
        option = _TAR_COMPRESSION_TO_OPTION.get(compression, "")

        command = (
            f"tar -x{option}f {file}"
            if to is None
            else f"tar -x{option}f {file} -C {to}"
        )

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ {command}")

        subprocess.run(command, shell=True, check=True)
        return

    except subprocess.CalledProcessError as e:

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ tar failed: {e}")

    except Exception as e:

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ Unexpected error occurred: {e}")

    mode = "r" if compression is None else f"r:{compression}"
    with tarfile.open(file, mode=mode) as tar:
        tar.extractall(to)


def _extract_zip_archive(
    file: pathlib.Path,
    to: pathlib.Path | None = None,
    compression: int | None = None,
    verbose: bool = False,
) -> None:
    """Extract a ZIP archive."""
    try:
        command = (
            f"unzip -oq {file}" if to is None else f"unzip -oq {file} -d {to}"
        )

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ {command}")

        subprocess.run(command, shell=True, check=True)
        return

    except subprocess.CalledProcessError as e:

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ unzip failed: {e}")

    except Exception as e:

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ Unexpected error occurred: {e}")

    compression = zipfile.ZIP_STORED if compression is None else compression
    with zipfile.ZipFile(file, mode="r", compression=compression) as zip:
        zip.extractall(to)


def extract_archive(
    file: str | pathlib.Path,
    to: str | pathlib.Path | None = None,
    remove: bool = False,
    verbose: bool = False,
) -> pathlib.Path:
    """
    Extract an archive.

    Supported archive formats for extraction:
    - tar
    - ZIP

    Args:
        file (str | pathlib.Path): The path to the archive to extract.
        to (str | pathlib.Path | None): The path to the directory where the archive will be extracted. If None, it will be extracted to the same directory as the archive.
        remove (bool): If True, remove the archive after extraction.
        verbose (bool): If True, enable verbosity.

    Returns:
        pathlib.Path: The path to the directory where the archive was extracted.
    """
    file = pathlib.Path(file)
    to = file.parent if to is None else pathlib.Path(to)

    # check if the archive exists and is a file
    if not file.exists():
        raise FileNotFoundError(f"Archive '{file}' does not exist.")
    if not file.is_file():
        raise ValueError(f"Archive '{file}' is not a file.")

    extension = _get_extension(file)

    # check if the archive has a valid extension
    if not extension:
        raise ValueError(f"Archive '{file}' has no extension.")
    if (
        extension not in _EXTENSION_TO_TAR_COMPRESSION
        and extension not in _EXTENSION_TO_ZIP_COMPRESSION
    ):
        raise ValueError(
            f"Archive '{file}' has an unknown extension '{extension}'."
        )

    if extension in _EXTENSION_TO_TAR_COMPRESSION:
        _extract_tar_archive(
            file, to, _EXTENSION_TO_TAR_COMPRESSION[extension], verbose
        )
    elif extension in _EXTENSION_TO_ZIP_COMPRESSION:
        _extract_zip_archive(
            file, to, _EXTENSION_TO_ZIP_COMPRESSION[extension], verbose
        )

    if verbose:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        print(f"[{timestamp}] ▶ Extracted the archive '{file}' to '{to}'")

    if remove:
        file.unlink()

        if verbose:
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
            print(f"[{timestamp}] ▶ Removed the archive '{file}'")

    return to
