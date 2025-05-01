import logging
import shutil
from http import HTTPStatus
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

import requests

from . import config

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


class HTTPDownloader:
    """
    Download a file over HTTP.
    May be overkill for our needs, but keeps the API consistent among
    S3, SFTP and HTTP.
    """

    @staticmethod
    def get_remote_file_path(filepath):
        """Returns the full remote path."""
        # Parse URL
        url_parts = urlparse(filepath)
        netloc = url_parts.netloc
        path = url_parts.path.lstrip("/")

        # If relative path, then prepend the base_url
        if not netloc:
            base_url = config.get("default", "base_url").rstrip("/")
            filepath = base_url + "/" + path
        return unquote(filepath)

    @staticmethod
    def download_file(remote_file, local_file):
        """Downloads a file over HTTP and saves it to disk."""
        if not Path(local_file).exists():
            # logger.debug('HTTP: %s ==> %s', remote_file, local_file)
            try:
                r = requests.get(remote_file, stream=True, timeout=10)
            except requests.exceptions.ConnectionError as e:
                logger.error(str(e))  # noqa: TRY400
                return False
            except requests.exceptions.Timeout as e:
                logger.error(str(e))  # noqa: TRY400
                return False

            if r.status_code != HTTPStatus.OK:
                logger.warning(
                    "%s does not exist. Status code=%s", remote_file, r.status_code
                )
                return False

            with Path(local_file).open("wb") as f:
                shutil.copyfileobj(r.raw, f)

            return True

        return False
