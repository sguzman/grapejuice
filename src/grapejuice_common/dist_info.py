import json
import logging
import os

from grapejuice_common import variables

LOG = logging.getLogger(__name__)


class DistributionType:
    source = "source"
    system_package = "system_package"


class DistributionInfo:
    def __init__(self, path: str = None):
        if path is None:
            path = os.path.join(variables.assets_dir(), "dist_info.json")

        self._path = path

        with open(self._path, "r") as fp:
            self._info = json.load(fp)

        LOG.debug(f"Loaded distribution info from {self._path}")
        LOG.info(f"Distribution type: {self.distribution_type}")

    def __getattr__(self, item):
        if item in self._info:
            return self._info[item]

        return super().__getattribute__(item)

    @property
    def distribution_type(self):
        k = "distribution_type"
        assert k in self._info

        v = self._info[k]
        assert isinstance(v, str)

        return v

    @distribution_type.setter
    def distribution_type(self, v: str):
        assert v in DistributionType.__dict__.values()
        self._info["distribution_type"] = v

    def write(self):
        with open(self._path, "w+") as fp:
            json.dump(self._info, fp)


dist_info = DistributionInfo()
