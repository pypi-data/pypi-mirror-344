import base64
import logging
import sys
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

import paramiko
import pysftp

from . import config
from . import utils

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


class SFTPDownloader:
    """Downloads a file from SFTP."""

    def __init__(self):
        self.config = dict(config.items("sftp"))
        try:
            self.sftp = pysftp.Connection(
                host=self.config["server"],
                username=self.config["username"],
                password=base64.b64decode(self.config["password"]),
            )
        except paramiko.ssh_exception.AuthenticationException as e:
            logger.error("SSH auth error: %s", e)  # noqa: TRY400
            utils.revert_manifest()
            utils.post_download()
            sys.exit(1)
        except paramiko.ssh_exception.SSHException as e:
            logger.error("SSH error: %s", e)  # noqa: TRY400
            utils.revert_manifest()
            utils.post_download()
            sys.exit(1)

    def get_remote_file_path(self, filepath):
        """Return the actual remote file path."""
        # Parse URL
        url_parts = urlparse(filepath)
        # netloc = url_parts.netloc
        path = url_parts.path.lstrip("/")

        # If it is a absolute or relative url doesn't matter, we need to
        # create the remote file path
        filepath = self.config["remote_dir"].rstrip("/") + "/" + path
        return unquote(filepath)

    def _download(self, remote_file, local_file):
        """Download helper to return True or False."""
        # logger.debug('SFTP: %s ==> %s', remote_file, local_file)
        try:
            self.sftp.get(remote_file, local_file, preserve_mtime=True)
            return True
        except OSError as e:
            logger.error(  # noqa: TRY400
                "%s@%s:%s does not exist. Status code=%s",
                self.config["username"],
                self.config["server"],
                remote_file,
                str(e),
            )
            return False

    def download_file(self, remote_file, local_file):
        """Downloads a file over SFTP and saves it to disk."""
        if not Path(local_file).exists():
            return self._download(remote_file, local_file)

        # File exists, if newer on remote: download it
        remote_file_mtime = self.sftp.stat(remote_file).st_mtime
        local_file_mtime = Path(local_file).stat().st_mtime
        if remote_file_mtime != local_file_mtime:
            return self._download(remote_file, local_file)
        return None

    def close(self):
        """Close SFTP connection."""
        # Close SFTP connection
        self.sftp.close()
