import argparse
import configparser
import logging
import logging.handlers
from pathlib import Path

from rich.logging import RichHandler

__version__ = "0.6.0"

# -----------------------------------------------------------------------------

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Downloads a manifest and its media files."
)
parser.add_argument("--config", help="Config file path", default="manifest-ingest.cfg")
# parser.add_argument('-p,', '--password', help='SFTP Password')
parser.add_argument("-m", "--mode", help="Force download mode", default="auto")
args = parser.parse_args()

# Read config
config_file = Path(args.config).expanduser()
config = configparser.ConfigParser()
config.read(config_file)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create logging format
msg_fmt = "[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s"
date_fmt = "%Y-%m-%d %I:%M:%S %p"
formatter = logging.Formatter(msg_fmt, date_fmt)

logfile = Path(config.get("default", "log")).expanduser()
if not logfile.parent.exists():
    logfile.parent.mkdir(parents=True)

fh = logging.handlers.RotatingFileHandler(
    logfile,
    maxBytes=10485760,
    backupCount=5,
)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

rh = RichHandler()
rh.setLevel(logging.DEBUG)

# Add logging handlers
logger.addHandler(fh)
# logger.addHandler(ch)
logger.addHandler(rh)
