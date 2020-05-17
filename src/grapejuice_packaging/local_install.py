import os
import subprocess
import tarfile
from pathlib import Path

from setuptools import Command

import grapejuice_common.variables as v
from grapejuice_common.task_sequence import TaskSequence

ROBLOX_STUDIO = "roblox-studio.desktop"
ROBLOX_PLAYER = "roblox-player.desktop"

MIME = {
    "x-scheme-handler/roblox-studio": ROBLOX_STUDIO,
    "x-scheme-handler/roblox-player": ROBLOX_PLAYER,
    "application/x-roblox-rbxl": ROBLOX_STUDIO,
    "application/x-roblox-rbxlx": ROBLOX_STUDIO
}


def _xdg_mime_default(desktop_entry: str, mime: str):
    subprocess.check_call(["xdg-mime", "default", desktop_entry, mime])


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
            "install", ".",
            "--user"
        ])

    @install.task("Updating MIME type associations")
    def update_mime_associations(log):
        for mime, desktop in MIME.items():
            log.info(f"Associating {mime} with {desktop}")
            _xdg_mime_default(desktop, mime)

    @install.task("Updating MIME database")
    def update_mime_database(log):
        path = Path(v.home(), ".local", "share", "mime").absolute()
        log.info(f"Updating MIME database: {path}")

        subprocess.check_call(["update-mime-database", str(path)])

    @install.task("Updating GTK icon cache")
    def update_icon_cache(log):
        subprocess.check_call(["gtk-update-icon-cache"])

    @install.task("Updating desktop database")
    def update_desktop_database(log):
        path = Path(v.home(), ".local", "share", "applications").absolute()
        log.info(f"Updating desktop database: {path}")

        subprocess.check_call(["update-desktop-database", str(path)])

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
