import io
import logging
import os
import shutil
import subprocess
import sys
import tarfile

import requests
from packaging import version

import grapejuice_common.variables as v
from grapejuice_common.updates.update_provider import UpdateProvider, UpdateError

LOG = logging.getLogger(__name__)


class SourceUpdateProvider(UpdateProvider):
    def target_version(self) -> version.Version:
        return UpdateProvider.gitlab_version(return_cached=True)

    def update_available(self) -> bool:
        return UpdateProvider.gitlab_version() > UpdateProvider.local_version()

    def local_is_newer(self) -> bool:
        return UpdateProvider.local_version() > UpdateProvider.gitlab_version(return_cached=True)

    @staticmethod
    def can_update() -> bool:
        return True

    def do_update(self):
        tmp_path = v.tmp_path()
        LOG.info(f"Temporary files path at: {tmp_path}")
        update_package_path = os.path.join(tmp_path, "update")

        response = requests.get(v.git_source_tarball())
        if response.status_code < 200 or response.status_code > 299:
            raise UpdateError(f"Received HTTP error {response.status_code} from GitLab")

        if os.path.exists(update_package_path):
            LOG.warning(f"Removing existing update package: {update_package_path}")
            shutil.rmtree(update_package_path, ignore_errors=True)

        else:
            LOG.debug(f"Creating update package directory: {update_package_path}")
            os.makedirs(update_package_path)

        fp = io.BytesIO(response.content)
        with tarfile.open(fileobj=fp) as tar:
            tar.extractall(update_package_path)

        cwd = os.getcwd()
        os.chdir(os.path.join(update_package_path, "grapejuice-master"))

        LOG.debug("Installing update")
        subprocess.check_call([sys.executable, "./install.py"])
        os.chdir(cwd)

        fp.close()
        del fp
        del response

        shutil.rmtree(tmp_path)
