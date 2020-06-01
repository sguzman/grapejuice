import os
import shutil
import subprocess
import sys
from pathlib import Path

import grapejuice_common.variables as v
from grapejuice_common.util.task_sequence import TaskSequence
from grapejuice_packaging import packaging_resources
from grapejuice_packaging.builders.package_builder import PackageBuilder


class AppImageBuilder(PackageBuilder):
    _script_name = "__main__"

    def build(self):
        assert os.path.exists("pyproject.toml") and os.path.isdir("src")

        app_image = TaskSequence("Build AppImage")
        app_dir = os.path.join(self._build_dir, "grapejuice.AppDir")
        pyinstaller_output_path = os.path.join(self._dist_dir, self._script_name)

        @app_image.task("Clean workspace")
        def clean(log):
            self.clean_build()
            self.clean_dist()

        @app_image.task("Run PyInstaller")
        def run_pyinstaller(log):
            script_path = os.path.join(os.path.abspath(os.getcwd()), "src", "grapejuice", f"{self._script_name}.py")
            log.info(f"Running PyInstaller on: {script_path}")

            subprocess.check_call([
                sys.executable, "-m", "PyInstaller",
                script_path
            ])

        @app_image.task("Strip binaries")
        def strip_binaries(log):
            pyinstaller_root = Path(pyinstaller_output_path)
            log.info(f"PyInstaller root: {pyinstaller_root}")

            rubbish = []

            for file in pyinstaller_root.rglob("*"):
                if "libstdc" in file.name.lower():
                    rubbish.append(file)

            for file in rubbish:
                path = str(file.absolute())
                log.info(f"Removing file: {path}")

                os.remove(path)

        @app_image.task("Prepare AppDir")
        def prepare_app_dir(log):
            log.info(f"AppDir is: {app_dir}")
            os.makedirs(app_dir, exist_ok=True)

            app_src = pyinstaller_output_path
            app_dst = os.path.join(app_dir, "app")
            log.info(f"Copying tree: {app_src} -> {app_dst}")

            shutil.copytree(app_src, app_dst)

        @app_image.task("Copy assets")
        def copy_assets(log):
            assets_src = v.assets_dir()
            assets_dst = os.path.join(app_dir, "app", "assets")
            log.info(f"Copying tree: {assets_src} -> {assets_dst}")

            shutil.copytree(assets_src, assets_dst)

        @app_image.task("Copy AppRun")
        def copy_app_run(log):
            src = packaging_resources.app_image_app_run()
            dst = os.path.join(app_dir, "AppRun")
            log.info(f"Copying AppRun: {src} -> {dst}")

            shutil.copy(src, dst)
            os.chmod(dst, 0o755)

        @app_image.task("Copy desktop entry")
        def copy_desktop_entry(log):
            src = packaging_resources.app_image_desktop()
            dst = os.path.join(app_dir, "grapejuice.desktop")
            log.info(f"Copying desktop entry: {src} -> {dst}")

            shutil.copy(src, dst)

        @app_image.task("Copy application icon")
        def copy_desktop_entry(log):
            src = v.grapejuice_icon()
            dst = os.path.join(app_dir, "grapejuice.svg")
            log.info(f"Copying icon: {src} -> {dst}")

            shutil.copy(src, dst)

        app_image.run()

    def dist(self):
        app_image = TaskSequence("Create Appimage distribution")
        app_dir = os.path.join(self._build_dir, "grapejuice.AppDir")
        app_dir_parent = os.path.dirname(app_dir)

        @app_image.task("Clean distribution folder again")
        def clean_dist(log):
            self.clean_dist()
            os.makedirs(self._dist_dir, exist_ok=True)

        @app_image.task("Run AppImage tool")
        def run_app_image_tool(log):
            log.info(f"Changing directory to: {app_dir_parent}")
            os.chdir(app_dir_parent)

            path = packaging_resources.app_image_tool()
            log.info(f"Using AppImage tool at: {path}")

            os.chmod(path, 0o755)
            subprocess.check_call([path, app_dir])

        @app_image.task("Move AppImage to dist folder")
        def move_app_image(log):
            for file in Path(app_dir_parent).rglob("*.AppImage"):
                shutil.move(str(file.absolute()), os.path.join(self._dist_dir, file.name))

        app_image.run()
