from enum import Enum


class DeploymentType(Enum):
    Source = 1
    PyPI = 2
    Snappy = 3
    AppImage = 4
    SystemPackage = 5


def deployment_type():
    return DeploymentType.Source
