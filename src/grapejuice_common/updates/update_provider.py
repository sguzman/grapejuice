import logging
import re
from abc import ABC, abstractmethod

import requests
from packaging import version

import grapejuice_common.variables as v
from grapejuice import __version__ as grapejuice_version

LOG = logging.getLogger(__name__)

VERSION_PTN = re.compile(r"__version__\s*=\s*\"([\d\.]+)\".*")


class UpdateError(RuntimeError):
    pass


class UpdateProvider(ABC):
    _cached_gitlab_version: version.Version = None

    @staticmethod
    def local_version() -> version.Version:
        return version.parse(grapejuice_version)

    @staticmethod
    def gitlab_version(return_cached: bool = False) -> version.Version:
        if return_cached and UpdateProvider._cached_gitlab_version is not None:
            return UpdateProvider._cached_gitlab_version

        url = v.git_grapejuice_init()
        response = requests.get(url)

        if response.status_code < 200 or response.status_code > 299:
            LOG.error(
                "Failed to get the version of grapejuice on GitLab. Returning version 0\n"
                f"URL: {url}\n"
                f"Response text: {response.text}\n"
            )

            return version.parse("0.0.0")

        for line in response.text.replace("\r", "").split("\n"):
            match = VERSION_PTN.match(line)
            if not match:
                continue

            ver = version.parse(match.group(1).strip())
            UpdateProvider._cached_gitlab_version = ver

            return ver

        LOG.error("Could not match a Grapejuice version string in the remote repository")
        LOG.warning("Returning version 0.0.0")

        return version.parse("0.0.0")

    @staticmethod
    def can_update() -> bool:
        return False

    @abstractmethod
    def do_update(self) -> None:
        pass

    @abstractmethod
    def update_available(self) -> bool:
        pass

    @abstractmethod
    def local_is_newer(self) -> bool:
        pass

    @abstractmethod
    def target_version(self) -> version.Version:
        pass
