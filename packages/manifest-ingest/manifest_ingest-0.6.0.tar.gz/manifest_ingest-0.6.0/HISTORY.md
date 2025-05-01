# History

All notable changes to this project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/).

## 0.6.0 (2025-04-30)

- Modernized the packaging
- Removed Python 2 support
- Add start of basic tests (better than nothing)

## 0.5.3 (2021-08-31)

- Updated packaging method, add Makefile for development, update setup.py

## 0.5.2 (2020-04-13)

- Added more complex regex to find key/value pairs where the value may be a URL or list of URLs

## 0.5.1 (2017-12-19)

- Bug fix with multiprocessing on Windows.

## 0.5.0 (2017-12-05)

- Bug fix with handling S3 downloads as the bucket name can be in the domain name or in the path (eg - bucket-name.s3.amazonaws.com or s3.amazonaws.com/bucket-name)

## 0.4.9 (2017-11-29)

- Bug fix and handle ports in IPs.

## 0.4.8 (2017-11-29)

- Support S3, SFTP and HTTP download URLs.

## 0.4.7 (2017-11-15)

- No changes. Version bump so we can remove older versions from test PyPi. Sorry.

## 0.4.6 (2017-11-15)

- No changes. Version bump so we can remove older versions from PyPi. Sorry.

---

## Undated updates

- **0.4.5** - Added Python 3.6+ support (still works with Python 2.7+)
- **0.4.4** - It's a mystery...
- **0.4.3** - Added multiprocessing to speed up downloads
- **0.4.2**
  - **Changed** Changed the way we look for keys with URLs (absolute or relative) to regex.
  - **Changed** Changed the way we strip URL prefixes to make paths relative (to to the download directory) to regex.
  - **Added** Added ability to specify AWS credenttial profile to use for S3 in config.
- **0.4.1** - Added ability to compare local and remote MD5 hashes to determine if a file is newer on S3.
- **0.4.0** - Complete refactor. Single entrypoint of `manifest-ingest`. Via config can handle S3, SFTP and HTTP manifest URL downloads.
- **0.3.6** - Update the way we save the manifest with s3 manifests.
- **0.3.5** - Added `manifest-s3` to handle manifests of S3 files.
- **0.3.4** - Lock in version of pysftp to 0.2.8 due to 0.2.9 HostKeys issue...again.
- **0.3.3** - Added `manifest_filename` config so we can save to custom named manifest file.
- **0.3.2** - After a failed SSH attempt, revert manifest to original and run post_download.
- **0.3.1** - Bug fix with creating remote path correctly on Windows.
- **0.3.0** - Revert to original manifest on SFTP login failure as we won't be able to download the files in the manifest.
- **0.2.9** - Lock in version of pysftp to 0.2.8 due to 0.2.9 HostKeys issue.
- **0.2.8** - Improved connection and SSH exception handling and added connection retries up to a max number of times.
- **0.2.7** - Due to complications with running via command line, we removed the Keychain/Credential Manager support. You may now pass passwords via Base64 to at least thwart over the shoulder attacks. Also changed the way we execute the post download command to be non-blocking.
- **0.2.6** - When executing `manifest-sftp` over SSH, Keychain/Credential Manager do not provide the password so we added the ability to manually provide a password via the `-p` or `--password` argument on the command line (use with caution)
- **0.2.5** - Use Keychain (OSX) or Credential Manager (Windows) to get SFTP password
- **0.2.4** - If manifest is empty (eg - {}), then we abort and do not launch post_download commands
- **0.2.3** - Removed some logging clutter
- **0.2.2** - Additional logging
- **0.2.1** - Fixed bug where local filename would be striped of the word "media"
- **0.2.0** - Key names are now a regex which is more flexible & powerful
- **0.1.3** - Added elapsed time to log
- **0.1.2** - Fixed remote path bug on Windows
- **0.1.1** - Fixed url path removal from JSON and correct os paths
- **0.1.0** - Fixed bug with run_command call typo
- **0.0.9** - Fixed bug with config setup importing from wrong package
- **0.0.8** - Fixed bug where we expected a api_token in the config (not always needed)
- **0.0.7** - Added single package entry point (all script entry points us same config) and Removed `manifest-quickstart`
- **0.0.6** - Major refactor to make more configurable
- **0.0.5** - Added alternate media URL strip method
- **0.0.4** - Added config option to launch command line app when download finished
- **0.0.3** - Graceful error handling for when a remote file doesn't exist and we attempt to download it
- **0.0.2** - Added saving and backup of manifest locally
- **0.0.1** - (2015) Initial release
