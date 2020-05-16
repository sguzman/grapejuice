import sys

from grapejuice_packaging.builders.linux_package_builder import LinuxPackageBuilder, LinuxPackageConfiguration


class LinuxSupplementalPackageBuilder(LinuxPackageBuilder):
    def __init__(self, build_dir, dist_dir, level_1_directory: str = ".local"):
        configuration = LinuxPackageConfiguration(build_dir)
        configuration.python_site_type = "site_packages"
        configuration.python_site_version = f"python{sys.version_info.major}.{sys.version_info.minor}"
        configuration.copy_packages = False
        configuration.level_1_directory = level_1_directory

        super().__init__(build_dir, dist_dir, configuration)
