import os
import shutil

from grapejuice_common import variables
from grapejuice_common.pid_file import daemon_pid_file
from grapejuice_common.settings import settings

EXCLUSIONS = ["venv", ".idea", ".git", "__pycache__", "wineprefix", ".gitignore"]

DESKTOP_STUDIO = "roblox-studio.desktop"
DESKTOP_PLAYER = "roblox-player.desktop"
DESKTOP_GRAPEJUICE = "grapejuice.desktop"

MIME_RBXL = "x-roblox-rbxl.xml"
MIME_RBXLX = "x-roblox-rbxlx.xml"


def copy_files(target):
    source = variables.src_dir()

    if not os.path.exists(target):
        os.makedirs(target)

    for f in os.listdir(source):
        if f in EXCLUSIONS:
            continue

        src_fp = os.path.join(source, f)
        dest_fp = os.path.join(target, f)

        if os.path.exists(dest_fp):
            shutil.rmtree(dest_fp, ignore_errors=True)

        if os.path.isfile(src_fp):
            shutil.copyfile(src_fp, dest_fp)
        elif os.path.isdir(src_fp):
            shutil.copytree(src_fp, dest_fp)


def run_shell_script(cwd, script):
    old_cwd = os.getcwd()
    os.chdir(cwd)

    os.spawnlp(os.P_WAIT, "bash", "bash", script)

    os.chdir(old_cwd)


def install_packages(target):
    run_shell_script(target, "install-packages.sh")


def set_bits(target):
    run_shell_script(target, "set-bits.sh")


def install_desktop_file(source, install_target, target_dir):
    name = os.path.basename(source)

    target = os.path.join(target_dir, name)
    if os.path.exists(target):
        os.remove(target)

    with open(source, "r") as source_file:
        lines = []
        for line in source_file.readlines():
            lines.append(line.replace("$APPLICATION_DIR", install_target))

        with open(target, "w+") as target_file:
            target_file.writelines(lines)


def desktop_entries():
    return [DESKTOP_GRAPEJUICE, DESKTOP_STUDIO, DESKTOP_PLAYER]


def install_desktop_files(install_target):
    applications_dir = variables.xdg_applications_dir()
    if not os.path.exists(applications_dir):
        os.makedirs(applications_dir)

    for entry in desktop_entries():
        install_desktop_file(
            os.path.join(variables.assets_dir(), entry),
            install_target,
            applications_dir
        )


def install_mime_def(src, target_dir):
    name = os.path.basename(src)

    target = os.path.join(target_dir, name)
    if os.path.exists(target):
        os.remove(target)

    shutil.copy(src, target)


def update_mime_database():
    xdg_mime = variables.xdg_mime_dir()
    if not os.path.exists(xdg_mime):
        os.makedirs(xdg_mime)

    os.spawnlp(os.P_WAIT, "update-mime-database", "update-mime-database", xdg_mime)


def mime_files():
    return [MIME_RBXL, MIME_RBXLX]


def install_mime_files():
    pkgs = variables.xdg_mime_packages()
    if not os.path.exists(pkgs):
        os.makedirs(pkgs)

    for f in mime_files():
        install_mime_def(os.path.join(variables.assets_dir(), f), pkgs)

    update_mime_database()


def mime_assoc(desktop, mime_type):
    os.spawnlp(os.P_WAIT, "xdg-mime", "xdg-mime", "default", desktop, mime_type)


def update_protocol_handlers():
    mime_assoc(DESKTOP_STUDIO, "x-scheme-handler/roblox-studio")
    mime_assoc(DESKTOP_PLAYER, "x-scheme-handler/roblox-player")


def update_file_associations():
    mime_assoc(DESKTOP_STUDIO, "application/x-roblox-rbxl")
    mime_assoc(DESKTOP_STUDIO, "application/x-roblox-rbxlx")


def post_install(install_target=variables.application_dir()):
    pid_file = daemon_pid_file()
    pid_file.kill()

    install_mime_files()
    install_desktop_files(install_target)
    update_protocol_handlers()
    update_file_associations()

    settings.performed_post_install = True
    settings.save()


def install_main(install_target=variables.application_dir()):
    abs_install_target = os.path.abspath(install_target)

    copy_files(abs_install_target)
    install_packages(abs_install_target)
    set_bits(abs_install_target)
    install_mime_files()
    install_desktop_files(abs_install_target)
    update_protocol_handlers()
    update_file_associations()
