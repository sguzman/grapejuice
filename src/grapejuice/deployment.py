import glob
import os
import shutil
import subprocess
from typing import Dict

from grapejuice_common import variables
from grapejuice_common.pid_file import daemon_pid_file
from grapejuice_common.settings import settings

K_GRAPEJUICE_EXECUTABLE = "GRAPEJUICE_EXECUTABLE"

DESKTOP_STUDIO = "roblox-studio.desktop"
DESKTOP_PLAYER = "roblox-player.desktop"

PROTOCOL_ASSOC = {
    "x-scheme-handler/roblox-studio": DESKTOP_STUDIO,
    "x-scheme-handler/roblox-player": DESKTOP_PLAYER
}

FILE_ASSOC = {
    "application/x-roblox-rbxl": DESKTOP_STUDIO,
    "application/x-roblox-rbxlx": DESKTOP_STUDIO
}


def log(*args):
    print("!!", *args)


def invoke_xdg_mime() -> bool:
    return not variables.is_packaging()


def get_desktop_install_path(desktop_name):
    return os.path.join(variables.xdg_applications_dir(), desktop_name)


def install_desktop_files(environ: Dict):
    assert isinstance(environ, dict)

    desktop_assets = variables.desktop_assets_dir()

    for desktop_name in os.listdir(desktop_assets):
        target_path = get_desktop_install_path(desktop_name)
        source_path = os.path.join(desktop_assets, desktop_name)

        target_directory = os.path.dirname(target_path)
        os.makedirs(target_directory, exist_ok=True)

        log("Installing desktop file", source_path, "to", target_path)

        def process_line(line):
            for k, v in environ.items():
                search_ptn = "$" + k
                if search_ptn in line:
                    line = line.replace(search_ptn, v)

            return line

        with open(source_path, "r") as source_fp:
            with open(target_path, "w+") as target_fp:
                output_lines = list(map(process_line, source_fp.readlines()))
                target_fp.writelines(output_lines)


def update_mime_database():
    if not invoke_xdg_mime():
        return

    log("Updating MIME database")
    xdg_mime = variables.xdg_mime_dir()

    os.makedirs(xdg_mime, exist_ok=True)
    subprocess.check_call(["update-mime-database", xdg_mime])


def install_mime_def(src, target_dir):
    log("Installing MIME definition", src, "into the directory", target_dir)
    name = os.path.basename(src)

    target = os.path.join(target_dir, name)
    assert target

    if os.path.exists(target):
        os.remove(target)

    shutil.copy(src, target)


def install_mime_files():
    mime_source = variables.mime_xml_assets_dir()
    mime_packages = variables.xdg_mime_packages()

    log("Installing MIME XML files from", mime_source, "into", mime_packages)

    os.makedirs(mime_packages, exist_ok=True)

    for file in glob.glob(os.path.join(mime_source, "*")):
        install_mime_def(file, mime_packages)

    update_mime_database()


def mime_assoc(desktop, mime_type):
    if not invoke_xdg_mime():
        return

    log("MIME assoc", desktop, mime_type)

    subprocess.check_call(["xdg-mime", "default", desktop, mime_type])


def update_protocol_handlers():
    log("Updating protocol handlers")

    for scheme, desktop in PROTOCOL_ASSOC.items():
        mime_assoc(desktop, scheme)


def update_file_associations():
    log("Updating file associations")

    for scheme, desktop in FILE_ASSOC.items():
        mime_assoc(desktop, scheme)


def install_icons():
    icons = glob.glob(os.path.join(variables.icons_assets_dir(), "**"), recursive=True)
    icons = list(filter(os.path.isfile, icons))

    common_prefix = variables.icons_assets_dir()

    rel_icons = list(map(lambda path: os.path.relpath(path, common_prefix), icons))

    for icon in rel_icons:
        src = os.path.join(common_prefix, icon)
        dst = os.path.join(variables.xdg_icons(), icon)
        log("Installing icon", src, dst)

        dst_parent = os.path.dirname(dst)
        os.makedirs(dst_parent, exist_ok=True)

        shutil.copy(src, dst)


def post_install():
    assert variables.K_GRAPEJUICE_INSTALL_PREFIX in os.environ

    def application_dir():
        if variables.is_packaging():
            return os.path.join(variables.packaging_prefix(), "share", "grapejuice")

        return variables.system_application_dir()

    def grapejuice_executable():
        if K_GRAPEJUICE_EXECUTABLE in os.environ:
            return os.environ[K_GRAPEJUICE_EXECUTABLE]

        return os.path.join(application_dir(), "bin", "grapejuice")

    environ = {
        variables.K_GRAPEJUICE_INSTALL_PREFIX: variables.installation_prefix(),
        "APPLICATION_DIR": application_dir(),
        K_GRAPEJUICE_EXECUTABLE: grapejuice_executable(),
        "GRAPEJUICE_ICON": "grapejuice",
        "STUDIO_ICON": "grapejuice-roblox-studio",
        "PLAYER_ICON": "grapejuice-roblox-player"
    }

    pid_file = daemon_pid_file()
    pid_file.kill()

    install_mime_files()
    install_icons()
    install_desktop_files(environ)
    update_protocol_handlers()
    update_file_associations()

    settings.performed_post_install = True
    settings.save()
