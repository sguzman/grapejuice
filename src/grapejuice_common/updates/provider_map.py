from grapejuice_common.dist_info import DistributionType, dist_info
from grapejuice_common.updates.source_update_provider import SourceUpdateProvider
from grapejuice_common.updates.system_update_provider import SystemUpdateProvider
from grapejuice_common.updates.update_provider import UpdateProvider

UPDATE_PROVIDER_MAP = {
    DistributionType.system_package: SystemUpdateProvider,
    DistributionType.source: SourceUpdateProvider
}


class NoUpdateProvider(RuntimeError):
    def __init__(self, dist_type: str):
        super().__init__(f"Could not resolve an update provider for distribution type {dist_type}")


def get_update_provider() -> UpdateProvider:
    dist_type = dist_info.distribution_type
    if dist_type in UPDATE_PROVIDER_MAP:
        return UPDATE_PROVIDER_MAP[dist_type]()

    raise NoUpdateProvider(dist_type)
