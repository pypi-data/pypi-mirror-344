# Manifest Ingest
Author: Tim Santor <tsantor@xstudios.com>

# Overview
Download a project JSON manifest and its media files via S3, SFTP or HTTP. This tool was developed for internal use on all X Studios interactive installations which need to have the ability to run "offline" when there is no active network connection.

# Installation
```
pip install manifest-ingest
```

> Note: On Windows Visual Studio C++ Build Tools 14 is required. You can install it with Chocolatey via: `choco install microsoft-visual-cpp-build-tools`

# Usage

## Create a Config file
Create a config file at `~/manifest-ingest.cfg`:

```ini
[default]
; API endpoint which returns JSON
api_url = http://192.168.1.69:8000/api/v1/music/playlist/
; Authorization header needed to access the API (optional)
api_token = Token API_TOKEN
; Regex of key names to search for
keys = (audio_url|artwork_url)
; Override the default manifest filename (optional)
manifest_filename = manifest.json
; Local directory to place downloaded files
local_dir = ~/target/dir/downloads
; Where to place the log file for the application
log = ~/target/dir/manifest-ingest.log
; Max retries to make failed network request before giving up
max_retries = 5
; Base URL for relative paths
base_url = http://192.168.1.69:8000
; Concurrent downloads (number of cores * 2 is usually best)
concurrent_downloads = 4

[s3]
profile_name = default
bucket_name = BUCKET_NAME
; Compare MD5 hash of local file with remote file
compare_md5 = true

[sftp]
server = 192.168.1.100
username = USERNAME
password = PASSWORD
; Remote directory on server to prepend to file URLs in manifest
remote_dir = /path/to/project

[post_download]
; Command to run when complete
command = osascript -e 'tell application "Safari" to activate'
```

> NOTE: The config file can be located anywhere that is readable by the user. The `s3`, `sftp` and `post_download` sections are optional.

## Usage

```bash
manifest-ingest --config=~/manifest-ingest.cfg
```

## Run at Startup (Mac)
Create a plist file as `/Library/LaunchAgents/com.user.manifestingest.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.manifestingest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/manifest-ingest</string>
        <string>--config</string>
        <string>~/config/manifest-ingest.cfg</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then run:

```bash
launchctl load /Library/LaunchAgents/com.user.manifestingest.plist
```

## Run at Startup (PC)
Create a Scheduled Task.

- **Triggers** - At log on of any user (Delay task for 30 secs)
- **Actions** - Start a Program: manifest-ingest --config="/Users/Admin/project/config/manifest-ingest.cfg"

On Windows, your bat file to launch a Unity app will look something like this:

```
START "" /D "C:\Users\Admin\Desktop\AppName" "AppName.exe" -screen-fullscreen 1 -screen-width 1920 -screen-height 1080
```
# Issues

If you experience any issues, please create an [issue](https://bitbucket.org/xstudios/manifest-ingest/issues) on Bitbucket.
