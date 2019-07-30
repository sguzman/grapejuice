import os
import shutil
import sys
import zipfile

import wget

import grapejuice_common.variables as variables


def perform_download():
    download_path = variables.tmp_zip_path()
    if os.path.exists(download_path):
        os.remove(download_path)

    return wget.download(
        variables.git_zip_download(),
        download_path
    )


def unpack_download(filename):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(variables.tmp_path())


def perform_update():
    filename = perform_download()
    if os.path.exists(filename):
        unpack_download(filename)

        srcdir = os.path.join(variables.tmp_path(), "grapejuice-master")
        if os.path.exists(srcdir):
            os.chdir(srcdir)
            os.spawnlp(os.P_WAIT, "python3", "python3", "./deployment.py")
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
    if perform_update():
        os.chdir(variables.src_dir())
        p = variables.run_script_path()
        if os.path.exists(p):
            delete_tmp()
            os.spawnlp(os.P_NOWAIT, p, p, "gui")
            sys.exit(0)
