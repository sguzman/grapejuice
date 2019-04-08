import os
import re
import shutil
import sys
import zipfile

import certifi
import urllib3 as u3
import wget
from packaging import version

import grapejuice._internal.variables as variables

VERSION_PATTERN = re.compile(r'__version__\s*=\s*"(.+)?".*')
HTTP = None

cached_remote_version = None


def http():
    global HTTP

    if HTTP is None:
        HTTP = u3.PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=certifi.where()
        )

    return HTTP


def local_version():
    version_string = None

    with open(variables.src_init_py(), "r") as file:
        for line in file.readlines():
            match = VERSION_PATTERN.match(line)
            if match:
                version_string = match.group(1)

    if version_string is None:
        return version_string

    return version.parse(version_string)


def remote_version():
    version_string = None
    r = http().request("GET", variables.git_init_py_url())
    if r.status == 200:
        version_string = str(r.data, "utf-8")

    if version_string is None:
        return version_string

    match = VERSION_PATTERN.match(version_string)
    if match is None:
        return None

    global cached_remote_version
    cached_remote_version = version.parse(match.group(1))

    return cached_remote_version


def update_available():
    local = local_version()
    if local is None:
        print("Warning: could not get the local version number")
        return False

    remote = remote_version()
    if remote is None:
        print("Warning: could not get the remote version number")
        return False

    return local < remote


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
    if perform_update():
        os.chdir(variables.src_dir())
        p = variables.run_script_path()
        if os.path.exists(p):
            delete_tmp()
            os.spawnlp(os.P_NOWAIT, p, p, "--gui")
            sys.exit(0)
