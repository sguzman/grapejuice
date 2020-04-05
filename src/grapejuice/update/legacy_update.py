import os
import shutil
import sys
import zipfile

import grapejuice_common.variables as variables
from grapejuice_common.pid_file import daemon_pid_file
from grapejuice_common.util import download_file


def perform_download():
    download_path = variables.tmp_zip_path()
    if os.path.exists(download_path):
        os.remove(download_path)

    return download_file(
        variables.git_zip_download(),
        download_path
    )


def unpack_download(filename):
    p = variables.tmp_path()
    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(p)

    except zipfile.BadZipFile as e:
        print(repr(e))
        return None

    return p


def perform_update():
    daemon_pid = daemon_pid_file()
    if daemon_pid.is_running():
        daemon_pid.kill()

    filename = perform_download()
    if os.path.exists(filename):
        download_dir = unpack_download(filename)
        if download_dir is None:
            return False

        src_dir = os.path.join(download_dir, "grapejuice-master")
        if os.path.exists(src_dir):
            os.chdir(src_dir)
            os.spawnlp(os.P_WAIT, "python3", "python3", "./install.py")
            return True

        else:
            return False
    else:
        return False


def delete_tmp():
    p = variables.tmp_path()
    if os.path.exists(p) and os.path.isdir(p):
        shutil.rmtree(p)


def update_and_reopen():
    src_dir = variables.src_dir()

    if perform_update():
        os.chdir(src_dir)
        delete_tmp()
        os.spawnlp(os.P_NOWAIT, "python3", "python3", "-m", "grapejuice", "gui")
        sys.exit(0)
