import re

from packaging import version

from grapejuice_common import variables
from grapejuice_common.http import http

VERSION_PATTERN = re.compile(r'__version__\s*=\s*"(.+)?".*')
cached_remote_version = None


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
