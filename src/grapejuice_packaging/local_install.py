import os
import subprocess
import tarfile
from pathlib import Path

from setuptools import Command

import grapejuice_common.variables as v
from grapejuice_common.task_sequence import TaskSequence


def _do_install(*_):
    assert os.path.exists("pyproject.toml"), \
        "Project file not found, make sure you're in the Grapejuice root!"

    src_path = os.path.join(os.path.abspath(os.getcwd()), "src")
    if "PYTHONPATH" in os.environ:
        os.environ["PYTHONPATH"] = src_path + ":" + os.environ["PYTHONPATH"]

    else:
        os.environ["PYTHONPATH"] = src_path

    install = TaskSequence("Install Grapejuice locally")

    @install.task("Build package of supplemental files")
    def build_supplemental(log):
        subprocess.check_call([
            "python3", "-m", "grapejuice_packaging",
            "supplemental_package"
        ])

    @install.task("Install supplemental packages")
    def install_supplemental_packages(log):
        for file in Path("dist", "supplemental_package").glob("*.tar.gz"):
            log.info(f"Installing supplemental package {file}")

            with tarfile.open(file) as tar:
                tar.extractall(v.home())

    @install.task("Install Grapejuice package")
    def install_package(log):
        subprocess.check_call([
            "python3", "-m", "pip",
            "install", "."
        ])

    install.run()


class InstallLocally(Command):
    description = "Install Grapejuice locally"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        _do_install(self.user_options)
