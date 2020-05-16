import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from string import Template

import grapejuice_common.variables as v
import grapejuice_packaging.packaging_resources as res
from grapejuice_common.task_sequence import TaskSequence
from grapejuice_packaging.builders.package_builder import PackageBuilder

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def _build_package(root):
    build_sequence = TaskSequence("Build Linux Package")

    @build_sequence.task("Copy packages to site")
    def copy_packages(log):
        python_site = Path(root, "usr", "lib", "python3", "dist-packages")
        log.info(f"Using site directory: {python_site}")
        os.makedirs(python_site, exist_ok=True)

        subprocess.check_call([
            "python3", "-m", "pip",
            "install", ".",
            "--no-dependencies",
            "--target", str(python_site)
        ])

    @build_sequence.task("Copy MIME files")
    def mime_files(log):
        mime_packages = Path(root, "usr", "share", "mime", "packages")
        log.info(f"Using mime packages directory: {mime_packages}")
        os.makedirs(mime_packages, exist_ok=True)

        for file in Path(v.mime_xml_assets_dir()).rglob("*.xml"):
            shutil.copyfile(str(file.absolute()), mime_packages.joinpath(file.name))

    @build_sequence.task("Copy icons")
    def copy_icons(log):
        icons = Path(root, "usr", "share", "icons")
        log.info(f"Using icons directory: {icons}")

        shutil.copytree(v.icons_assets_dir(), icons)

    @build_sequence.task("Copy desktop entries")
    def copy_desktop_files(log):
        xdg_applications = Path(root, "usr", "share", "applications")
        log.info(f"Using XDG applications directory: {xdg_applications}")
        os.makedirs(xdg_applications, exist_ok=True)

        desktop_variables = {
            "GRAPEJUICE_ICON": "grapejuice",
            "GRAPEJUICE_EXECUTABLE": "/usr/bin/grapejuice",
            "PLAYER_ICON": "grapejuice-roblox-player",
            "STUDIO_ICON": "grapejuice-roblox-studio"
        }

        for file in Path(v.desktop_assets_dir()).rglob("*.desktop"):
            with file.open("r") as fp:
                template = Template(fp.read())
                finished_desktop_entry = template.substitute(desktop_variables)

            target_path = xdg_applications.joinpath(file.name)
            with target_path.open("w+") as fp:
                fp.write(finished_desktop_entry)

    @build_sequence.task("Copy binary entries")
    def copy_bin_scripts(log):
        usr_bin = Path(root, "usr", "bin")
        log.info(f"Using bin directory: {usr_bin}")
        os.makedirs(usr_bin, exist_ok=True)

        shutil.copyfile(res.bin_grapejuice_path(), usr_bin.joinpath("grapejuice"))
        shutil.copyfile(res.bin_grapejuiced_path(), usr_bin.joinpath("grapejuiced"))

    build_sequence.run()


class LinuxPackageBuilder(PackageBuilder):
    def build(self):
        self.clean_build()
        self._prepare_build()

        _build_package(self._build_dir)

    def dist(self):
        pass
