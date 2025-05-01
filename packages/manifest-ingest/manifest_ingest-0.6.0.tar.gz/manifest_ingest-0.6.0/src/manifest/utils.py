import hashlib
import json
import logging
import re
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path

import requests
from tenacity import before_sleep_log
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_exponential

from . import config

# -----------------------------------------------------------------------------

logger = logging.getLogger(__name__)
current_retries = 0


def post_download():
    """Post download action. Run a command."""
    if not config.has_section("post_download"):
        return

    post_cfg = dict(config.items("post_download"))
    subprocess.run(shlex(post_cfg["command"]), check=True)  # noqa: S603


def find_all_keys(obj, keys: str) -> list:
    """Find all target keys with URLs in parsed JSON."""
    # Pre-compile regex for better performance
    pattern = re.compile(
        rf'"(?P<key>{keys})":\s*'  # Match key
        r"(?P<value>"
        r'\["(?P<list_value>(https?://|/).+?)"(?:,\s*"(?:https?://|/).+?")*\]|'  # List of URLs
        r'"(?P<url_value>(https?://|/).+?)"'  # Single URL
        r")",
        re.MULTILINE,
    )

    results = set()
    json_str = json.dumps(obj, separators=(",", ":"))  # Minimize JSON string

    for match in pattern.finditer(json_str):
        if match.group("list_value"):
            # Handle list of URLs
            list_values = json.loads(match.group("value"))
            results.update(x for x in list_values if x)
        elif match.group("url_value"):
            # Handle single URL
            url = match.group("url_value")
            if url:
                results.add(url)

    logger.debug("Found %s unique files matching keys: %s", len(results), keys)
    return sorted(results)


@retry(
    stop=stop_after_attempt(config.getint("default", "max_retries", fallback=3)),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type(
        (
            requests.ConnectionError,
            requests.Timeout,
            requests.exceptions.ChunkedEncodingError,
        )
    ),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def get_manifest():
    """Fetch manifest from API with exponential backoff retries.

    Returns:
        Dict[str, Any]: Parsed JSON response or None if unrecoverable error occurs.
    """
    url = config.get("default", "api_url")
    token = config.get("default", "api_token", fallback=None)

    logger.info("Fetching manifest from %s", url)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    params = {"format": "json"}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=(3.05, 30),  # Connect and read timeouts
        )
        response.raise_for_status()
        return response.json()

    except requests.HTTPError as err:
        logger.error("HTTP Error %s: %s", err.response.status_code, err)  # noqa: TRY400
        if err.response.status_code >= 500:  # noqa: PLR2004
            # Retry on server errors (will be caught by tenacity)
            raise
        # Client errors (4xx) shouldn't be retried
        post_download()
        return None

    except requests.RequestException as err:
        logger.error("Request failed: %s", err)  # noqa: TRY400
        # This will be retried by tenacity
        raise


def get_manifest_filename():
    """Get the manifest filename safely for backwards compat.
    e.g. - `manifest_filename` is missing from the config file."""
    if config.has_option("default", "manifest_filename"):
        return config.get("default", "manifest_filename")
    return "manifest.json"


def backup_manifest():
    """Backup current manifest with atomic write operation.

    Returns:
        Path: Path to backup file if created, None otherwise
    """
    manifest_path = (
        Path(config.get("default", "local_dir")).expanduser() / get_manifest_filename()
    )
    backup_path = manifest_path.with_suffix(".bak")

    if not manifest_path.exists():
        logger.debug("No manifest found at %s", manifest_path)
        return None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            temp_path = Path(tmp.name)
            shutil.copy2(manifest_path, temp_path)

        # Ensure the temporary file is closed before replacing
        temp_path.replace(backup_path)  # Atomic on POSIX systems
        logger.debug("Created backup at %s", backup_path)
        return backup_path

    except OSError as e:
        logger.error("Backup failed: %s", e)  # noqa: TRY400
        temp_path.unlink(missing_ok=True)
        return None


def save_manifest(json_content) -> None:
    """Saves manifest with URL normalization and proper error handling.

    Args:
        json_content: The JSON content to save
    """
    local_dir = Path(config.get("default", "local_dir")).expanduser()
    filepath = local_dir / get_manifest_filename()

    logger.debug('Saving manifest to "%s"', filepath)

    try:
        # Create parent directories if they don't exist
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Compile regex patterns once for better performance
        ip_port_pattern = re.compile(
            r': "(https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,4})'
        )
        protocol_pattern = re.compile(r': "(https?://|/)')

        # Process JSON with streaming for large files
        with filepath.open("w", encoding="utf-8") as f:
            # Convert to JSON string first
            json_content = (
                json_content.get("data") if "data" in json_content else json_content
            )
            json_str = json.dumps(json_content, sort_keys=True, indent=4)

            # Apply transformations
            json_str = ip_port_pattern.sub(r': "\1_\2', json_str)
            json_str = protocol_pattern.sub(r': "', json_str)

            f.write(json_str)

    except OSError as e:
        logger.error("Failed to save manifest: %s", e)  # noqa: TRY400
        raise
    except Exception as e:
        logger.error("Unexpected error saving manifest: %s", e)  # noqa: TRY400
        raise


def revert_manifest() -> bool:
    """Revert to backup manifest using atomic operations.

    Returns:
        bool: True if reversion succeeded, False otherwise
    """
    manifest_dir = Path(config.get("default", "local_dir")).expanduser()
    backup_path = manifest_dir / f"{get_manifest_filename()}.bak"
    manifest_path = manifest_dir / get_manifest_filename()

    if not backup_path.exists():
        logger.debug("No backup manifest found at %s", backup_path)
        return False

    try:
        # Atomic replacement using temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tmp") as tmp:
            temp_path = Path(tmp.name)
            shutil.copy2(backup_path, temp_path)
            temp_path.replace(manifest_path)  # Atomic operation

        backup_path.unlink(missing_ok=True)  # Clean up backup
        logger.debug("Successfully reverted to backup manifest")
        return True

    except OSError as e:
        logger.error("Failed to revert manifest: %s", e)  # noqa: TRY400
        # Clean up temp file if it exists
        if "temp_path" in locals():
            temp_path.unlink(missing_ok=True)
        return False


def md5_hash(filepath, chunk_size: int = 65536) -> str:
    """Calculate MD5 hash of a file efficiently"""
    md5sum = hashlib.md5()  # noqa: S324
    filepath = Path(filepath)
    with filepath.open("rb") as f:
        while chunk := f.read(chunk_size):
            md5sum.update(chunk)
    return md5sum.hexdigest()
