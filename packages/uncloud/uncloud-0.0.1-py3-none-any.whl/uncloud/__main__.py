import argparse

from .uncloud import uncloud


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="uncloud",
        description="Download (and extract) a public archive file from popular cloud storage services such as Dropbox, Google Drive, and OneDrive.",
    )
    parser.add_argument(
        "url",
        type=str,
        help="The share link URL of the archive file to download.",
    )
    parser.add_argument(
        "-D",
        "--download-to",
        type=str,
        default=None,
        metavar="DIR",
        help="The path to the directory where the archive file will be downloaded.",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="The filename of the archive file to download.",
    )
    parser.add_argument(
        "--hash",
        type=str,
        default=None,
        help="The MD5 checksum of the archive file for integrity verification.",
    )
    parser.add_argument(
        "-x",
        "--extract",
        action="store_true",
        help="Extract the archive file after downloading.",
    )
    parser.add_argument(
        "-X",
        "--extract-to",
        type=str,
        default=None,
        metavar="DIR",
        help="The path to the directory where the archive file will be extracted.",
    )
    parser.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="Remove the archive file after extraction.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbosity.",
    )
    args = parser.parse_args()

    uncloud(
        args.url,
        download_to=args.download_to,
        filename=args.filename,
        md5=args.hash,
        extract=args.extract,
        extract_to=args.extract_to,
        remove=args.remove,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    main()
