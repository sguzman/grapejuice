import os
from abc import ABC, abstractmethod

from grapejuice.update import legacy_update
from grapejuice_common.dist_info import DistributionType, dist_info

K_DISTRIBUTION_TYPE = "GRAPEJUICE_DISTRIBUTION_TYPE"


class UpdateProvider(ABC):
    @staticmethod
    @abstractmethod
    def can_update():
        raise NotImplementedError()

    @staticmethod
    def should_version_check():
        return False

    def do_update(self):
        pass

    def reinstall(self):
        pass


class SourceUpdateProvider(UpdateProvider):
    def can_update(self):
        return True

    def reinstall(self):
        legacy_update.update_and_reopen()

    def do_update(self):
        legacy_update.update_and_reopen()


class SystemPackageUpdateProvider(UpdateProvider):
    def can_update(self):
        return False


UPDATE_PROVIDER_MAPPING = {
    DistributionType.source: SourceUpdateProvider,
    DistributionType.system_package: SystemPackageUpdateProvider
}


def get_distribution_type():
    if K_DISTRIBUTION_TYPE in os.environ:
        return os.environ[K_DISTRIBUTION_TYPE]

    return dist_info.distribution_type


provider: UpdateProvider = UPDATE_PROVIDER_MAPPING[get_distribution_type()]()
