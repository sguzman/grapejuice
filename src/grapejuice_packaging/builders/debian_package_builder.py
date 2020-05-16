import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import grapejuice.__about__ as about
from grapejuice_common.task_sequence import TaskSequence
from grapejuice_packaging.builders.linux_package_builder import LinuxPackageBuilder
from grapejuice_packaging.util.distribution_detect import is_debian

ARCHITECTURE = "amd64"
STANDARDS_VERSION = "3.9.6"
DEBHELPER_COMPAT = 10
VERSION = f"{about.package_version}"
PACKAGE_VERSION = f"{VERSION}_{ARCHITECTURE}"
PREFIX = "/usr"
USR_LIB = os.path.join(PREFIX, "lib")
PYTHON_DIST_PACKAGES_DIR = f"{USR_LIB}/python3/dist-packages"
MAINTAINER = f"{about.author_name} <{about.author_email}>"
PACKAGE_FILENAME = f"{about.package_name}-{PACKAGE_VERSION}.deb"
DEBIAN_SECTION = "python"
DEBIAN_PRIORITY = "optional"
DEBIAN_DISTRIBUTION = "unstable"
DEBIAN_URGENCY = "medium"

FIELD_SOURCE = ("Source", about.package_name)
FIELD_MAINTAINER = ("Maintainer", MAINTAINER)
FIELD_STANDARDS_VERSION = ("Standards-Version", STANDARDS_VERSION)
FIELD_ARCHITECTURE = ("Architecture", ARCHITECTURE)
FIELD_BUILD_DEPENDS = ("Build-Depends", [
    "debhelper",
    "python3",
    "python3-pip",
    "python3-virtualenv",
    "git", "unzip"
])

CONTROL_FIELDS = [
    FIELD_SOURCE,
    ("Section", DEBIAN_SECTION),
    ("Priority", DEBIAN_PRIORITY),
    FIELD_MAINTAINER,
    FIELD_BUILD_DEPENDS,
    FIELD_STANDARDS_VERSION,
    None,
    ("Package", about.package_name),
    FIELD_ARCHITECTURE,
    ("Depends", [
        "python3 (>= 3.7~)",
        "python3-dbus",
        "python3-packaging",
        "python3-psutil",
        "python3-requests",
        "python3-gi",
        "libcairo2",
        "libgirepository-1.0-1",
        "libgtk-3-0",
        "libgtk-3-bin",
        "libdbus-1-3",
        "gobject-introspection",
        "gir1.2-gtk-3.0"
    ]),
    ("Homepage", about.package_repository),
    ("Description", about.package_description + "\n Generated by grapejuice_packaging")
]

COPYRIGHT_FIELDS = [
    ("Format", "https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/"),
    ("Upstream-Name", about.project_name),
    ("Upstream-Contact", MAINTAINER),
    FIELD_SOURCE,
    None,
    ("Files", "*"),
    ("Copyright", f"2019-{datetime.now().year} {about.author_name}"),
    ("License", about.package_license)
]

RULES = """#!/usr/bin/make -f

%:
\tdh $@

override_dh_shlibdeps:
\ttrue
"""


def _fields_to_string(fields):
    def process_field(field):
        if field is None:
            return ""

        assert isinstance(field, tuple) or isinstance(field, list)
        assert len(field) == 2

        key, value = field

        if isinstance(value, list):
            value = ", ".join(value)

        return f"{key}: {str(value)}"

    return "\n".join(list(map(process_field, fields)))


class DebianPackageBuilder(LinuxPackageBuilder):
    def build(self):
        self.clean_build()
        self._prepare_build()

        self._build_dir = os.path.join(self._build_dir, "pkg")

        super_build = super().build
        build = TaskSequence("Build Debian Package")

        @build.task("Create the base linux package")
        def create_linux_package(log):
            build_root = self._build_dir
            self._build_dir = os.path.join(build_root, "ROOT")

            super_build()

            self._build_dir = build_root

        @build.task("Create debian directory")
        def create_debian_directory(log):
            path = Path(self._build_dir, "debian")
            os.makedirs(path, exist_ok=True)

        @build.task("Write compat file")
        def write_compat(log):
            path = Path(self._build_dir, "debian", "compat")

            with path.open("w+") as fp:
                fp.write(str(int(DEBHELPER_COMPAT)))

        @build.task("Write install file")
        def write_compat(log):
            path = Path(self._build_dir, "debian", "install")

            with path.open("w+") as fp:
                content = "ROOT/* /\n"
                fp.write(content)

        @build.task("Write control file")
        def write_control(log):
            path = Path(self._build_dir, "debian", "control")

            with path.open("w+") as fp:
                fp.write(_fields_to_string(CONTROL_FIELDS))

        @build.task("Write copyright file")
        def write_copyright(log):
            path = Path(self._build_dir, "debian", "copyright")

            with path.open("w+") as fp:
                fp.write(_fields_to_string(COPYRIGHT_FIELDS))

        @build.task("Write files file")
        def write_files(log):
            path = Path(self._build_dir, "debian", "files")

            with path.open("w+") as fp:
                fp.write(" ".join([PACKAGE_FILENAME, DEBIAN_SECTION, DEBIAN_PRIORITY]))

        @build.task("Write rules file")
        def write_rules(log):
            path = Path(self._build_dir, "debian", "rules")

            with path.open("w+") as fp:
                fp.write(RULES)

        @build.task("Write changelog file")
        def write_changelog(log):
            lines = [f"{about.package_name} ({VERSION}) {DEBIAN_DISTRIBUTION}; urgency={DEBIAN_URGENCY}\n", "\n"]

            try:
                changelog = subprocess.check_output(["git", "shortlog"], timeout=1) \
                    .decode("UTF - 8").strip().split("\n")

            except subprocess.TimeoutExpired as e:
                changelog = ["Automatically generated package"]
                print(str(e))

            for changelog_line in list(map(lambda s: "  * " + s, changelog)):
                lines.append(changelog_line + "\n")

            lines.append("\n")

            date_str = datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " +0000"
            lines.append(f" -- {MAINTAINER}  {date_str}\n")

            with open(os.path.join(self._build_dir, "debian", "changelog"), "w+") as fp:
                fp.writelines(lines)

        build.run()

    def dist(self):
        self.clean_dist()
        self._prepare_dist()

        dist = TaskSequence("Create distribution files for debian")

        @dist.task("Strip out __pycache__ directories")
        def strip_py_cache(log):
            for directory in Path(self._build_dir).rglob("__pycache__"):
                if directory.is_dir():
                    log.info(f"Removing {directory}")
                    shutil.rmtree(directory, ignore_errors=True)

        if is_debian():
            wd = os.getcwd()

            @dist.task("Create package file")
            def create_package(log):
                os.chdir(self._build_dir)
                subprocess.check_call(["debuild", "-uc", "-us"])
                os.chdir(wd)

        @dist.task("Move distribution files")
        def move_files(log):
            for file in Path(self._build_dir).glob("*"):
                if file.is_file():
                    src = str(file.absolute())
                    dst = Path(self._dist_dir, file.name)

                    log.info(f"Moving file {src} -> {dst}")
                    shutil.move(src, dst)

        dist.run()
