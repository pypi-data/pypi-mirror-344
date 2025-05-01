import datetime
import logging
import multiprocessing
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from . import config
from . import utils
from .httpdownloader import HTTPDownloader
from .s3downloader import S3Downloader
from .sftpdownloader import SFTPDownloader

logger = logging.getLogger(__name__)

DEFAULT_CONCURRENT_DOWNLOADS = 10


def download_file(files: tuple[str, str], downloader_type: str) -> None:
    """Helper to allow multiprocessing."""
    remote_file, local_file = files

    try:
        if downloader_type == "s3":
            if config.has_section("s3"):
                # logger.info("Using S3 downloader")
                s3 = S3Downloader()
                s3.download_file(remote_file, local_file)
        elif downloader_type == "sftp":
            if config.has_section("sftp"):
                # logger.info("Using SFTP downloader")
                sftp = SFTPDownloader()
                sftp.download_file(remote_file, local_file)
        elif downloader_type == "http":
            # logger.info("Using HTTP downloader")
            HTTPDownloader.download_file(remote_file, local_file)
    except Exception as e:  # noqa: BLE001
        logger.error("Failed to download %s: %s", remote_file, e)  # noqa: TRY400


def run() -> None:  # noqa: C901, PLR0912, PLR0915
    """Run script."""
    start_time = time.time()
    logger.debug("-" * 10)

    # Initialize downloaders if needed
    sftp = SFTPDownloader() if config.has_section("sftp") else None
    s3 = S3Downloader() if config.has_section("s3") else None

    # Prepare local directory
    local_dir = Path(config.get("default", "local_dir")).expanduser()
    local_dir.mkdir(parents=True, exist_ok=True)

    # Handle manifest
    utils.backup_manifest()
    parsed_json = utils.get_manifest()

    if not parsed_json:
        logger.warning("Empty manifest. Aborting...")
        sys.exit(1)

    utils.save_manifest(parsed_json)

    # Find files to download
    keys = config.get("default", "keys")
    file_list = utils.find_all_keys(parsed_json, keys)
    file_list.sort()

    # Prepare download arguments
    s3_args = []
    http_args = []
    concurrent_downloads = config.getint(
        "default", "concurrent_downloads", fallback=DEFAULT_CONCURRENT_DOWNLOADS
    )

    for filepath in file_list:
        url_parts = urlparse(filepath)
        netloc = url_parts.netloc.replace(":", "_")
        path = url_parts.path.lstrip("/")

        local_file = local_dir / netloc / path
        local_file.parent.mkdir(parents=True, exist_ok=True)

        if "s3.amazonaws.com" in netloc:
            if s3 and (s3.bucket_name in netloc or s3.bucket_name in path):
                remote_file = s3.get_remote_file_path(path)
                s3_args.append((remote_file, str(local_file)))
            else:
                remote_file = HTTPDownloader.get_remote_file_path(filepath)
                http_args.append((remote_file, str(local_file)))
        elif sftp:
            remote_file = sftp.get_remote_file_path(filepath)
            sftp.download_file(remote_file, str(local_file))
        else:
            remote_file = HTTPDownloader.get_remote_file_path(filepath)
            http_args.append((remote_file, str(local_file)))

    # Process downloads with multiprocessing if enabled
    try:
        if concurrent_downloads > 1:
            logger.debug(
                "Using multiprocessing with %s concurrent downloads",
                concurrent_downloads,
            )
            with multiprocessing.Pool(processes=concurrent_downloads) as pool:
                pool.starmap(download_file, [(args, "s3") for args in s3_args])
                pool.starmap(download_file, [(args, "http") for args in http_args])
        else:
            for args in s3_args:
                download_file(args, "s3")
            for args in http_args:
                download_file(args, "http")
    except KeyboardInterrupt:
        logger.warning("Download interrupted by user. Terminating...")
        if "pool" in locals():
            pool.terminate()
        sys.exit(1)

    # Cleanup
    if sftp:
        sftp.close()

    elapsed = str(datetime.timedelta(seconds=(time.time() - start_time)))
    logger.debug("Time Elapsed: %s", elapsed)

    # Run post-download command
    try:
        utils.post_download()
    except Exception as e:  # noqa: BLE001
        logger.error("Post-download command failed: %s", e)  # noqa: TRY400


if __name__ == "__main__":
    run()
