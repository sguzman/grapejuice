import logging
import os
import time
from datetime import datetime
from glob import glob
from zipfile import ZipFile, ZIP_LZMA

from grapejuice_common import variables

LOG = logging.getLogger(__name__)
N_KEEP_LOGS = 10


def log_files():
    return glob(os.path.join(variables.logging_directory(), "*.log"))


def archive_directory():
    return os.path.join(variables.logging_directory(), "archive")


def archive_files():
    return glob(os.path.join(archive_directory(), "*.zip"))


def archive_logs(old_log_files):
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(archive_directory(), exist_ok=True)
    archive_path = os.path.join(archive_directory(), f"{datetime_now}.zip")

    LOG.info(f"Writing log archive {archive_path}")

    with ZipFile(archive_path, "w", ZIP_LZMA) as zf:
        for file in old_log_files:
            with open(file, "rb") as fp:
                zf.writestr(os.path.basename(file), fp.read(), ZIP_LZMA)

    for file in old_log_files:
        LOG.debug(f"Removing log file {file}")
        os.remove(file)


def can_delete_archive(file):
    stat = os.stat(file)
    time_delta = int(time.time()) - int(stat.st_ctime)

    # Older than a week
    return time_delta > 604800


def vacuum_logs():
    files = log_files()

    if len(files) >= 50:
        files.sort(key=lambda f: os.stat(f).st_ctime)
        old_files = files[:-N_KEEP_LOGS]
        archive_logs(old_files)

    for file in filter(can_delete_archive, archive_files()):
        LOG.info(f"Removing log archive {file}")
        os.remove(file)
