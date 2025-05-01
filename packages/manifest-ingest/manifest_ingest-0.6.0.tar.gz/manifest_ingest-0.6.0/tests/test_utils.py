import configparser
import hashlib
import io
import json
import shutil

import pytest

from manifest.utils import find_all_keys
from manifest.utils import md5_hash

# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------

CONFIG_INI = """
[default]
manifest_filename = manifest.json
api_url = https://domain.com/api/v1/timeline/manifest/
api_token = Token HERE
keys = (image)
local_dir = ~/Desktop/StreamingAssets
log = ~/.domain/manifest-ingest.log
max_retries = 5
base_url = https://domain.com
concurrent_downloads = 10

[s3]
profile_name = default
bucket_name = domain
compare_md5 = true
"""


@pytest.fixture
def mock_config(mocker):
    # Mock the open function to return the StringIO object
    mocker.patch("builtins.open", return_value=io.StringIO(CONFIG_INI))

    config = configparser.ConfigParser()
    config.read("fake_config.ini")
    return config


def test_config_values(mock_config):
    # Test the config values
    assert mock_config["default"]["manifest_filename"] == "manifest.json"
    assert (
        mock_config["default"]["api_url"]
        == "https://domain.com/api/v1/timeline/manifest/"
    )
    assert mock_config["s3"]["bucket_name"] == "domain"
    assert mock_config["s3"].getboolean("compare_md5") is True
    assert mock_config["default"].getint("max_retries") == 5  # noqa: PLR2004


@pytest.fixture
def sample_manifest(tmp_path):
    """Create a sample manifest file for testing."""
    manifest_data = {
        "data": {
            "files": [
                "http://example.com/file1.txt",
                "http://example.com/file2.txt",
            ],
            "nested": {
                "image_url": "http://example.com/image.png",
                "url_list": [
                    "http://example.com/list1.txt",
                    "http://example.com/list2.txt",
                ],
            },
        }
    }
    manifest_path = tmp_path / "test_manifest.json"
    with manifest_path.open("w") as f:
        json.dump(manifest_data, f)
    return manifest_path


@pytest.fixture
def sample_backup(tmp_path, sample_manifest):
    """Create a backup of the sample manifest."""
    backup_path = sample_manifest.with_suffix(".bak")
    shutil.copy2(sample_manifest, backup_path)
    return backup_path


# # -----------------------------------------------------------------------------
# # Tests
# # -----------------------------------------------------------------------------


def test_find_all_keys():
    """Test finding all keys with URLs in JSON."""
    test_data = {
        "image_url": "http://example.com/image.png",
        "urls": [
            "http://example.com/list1.txt",
            "http://example.com/list2.txt",
        ],
        "nested": {
            "file_url": "http://example.com/file.txt",
            "other": "not_a_url",
        },
    }

    # Test single key
    result = find_all_keys(test_data, "image_url")
    assert result == ["http://example.com/image.png"]

    # Test multiple keys
    result = find_all_keys(test_data, "image_url|file_url")
    assert sorted(result) == sorted(
        [
            "http://example.com/image.png",
            "http://example.com/file.txt",
        ]
    )

    # Test list of URLs
    result = find_all_keys(test_data, "urls")
    assert result == [
        "http://example.com/list1.txt",
        "http://example.com/list2.txt",
    ]

    # Test no matches
    result = find_all_keys(test_data, "nonexistent")
    assert result == []


def test_md5_hash(tmp_path):
    """Test MD5 hash calculation."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")

    # Known MD5 of "hello world"
    expected_hash = "5eb63bbbe01eeed093cb22bb8f5acdc3"
    assert md5_hash(test_file) == expected_hash


def test_md5_hash_large_file(tmp_path):
    """Test MD5 hash calculation with chunked reading."""
    # Create a file larger than the default chunk size
    test_file = tmp_path / "large.bin"
    data = b"0" * (65536 * 2)  # 2 chunks
    test_file.write_bytes(data)

    # Calculate expected hash
    md5 = hashlib.md5()  # noqa: S324
    md5.update(data)
    expected_hash = md5.hexdigest()

    assert md5_hash(test_file) == expected_hash
