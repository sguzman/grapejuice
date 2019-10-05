from enum import Enum


class DeploymentType(Enum):
    SOURCE = 1
    PYPI = 2
    SNAP = 3
    SYSTEM_PACKAGE = 4


def deployment_type():
    return DeploymentType.SOURCE
