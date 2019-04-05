#!/usr/bin/env python3

import inspect
import os
import shutil

import variables

EXCLUSIONS = ["venv", ".idea", ".git", "__pycache__", "wineprefix", ".gitignore"]

DESKTOP_STUDIO = "roblox-studio.desktop"
DESKTOP_PLAYER = "roblox-player.desktop"
DESKTOP_GRAPEJUICE = "grapejuice.desktop"


def copy_files():
    source = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    target = variables.application_dir()

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


def install_packages():
    old_cwd = os.getcwd()
    os.chdir(variables.application_dir())

    os.spawnlp(os.P_WAIT, "bash", "bash", "install-packages.sh")

    os.chdir(old_cwd)


def install_desktop_file(source, target_dir):
    name = os.path.basename(source)

    target = os.path.join(target_dir, name)
    if os.path.exists(target):
        os.remove(target)

    with open(source, "r") as source_file:
        lines = []
        for line in source_file.readlines():
            lines.append(line.replace("$APPLICATION_DIR", variables.application_dir()))

        with open(target, "w+") as target_file:
            target_file.writelines(lines)


def install_desktop_files():
    applications_dir = variables.xdg_applications_dir()
    if not os.path.exists(applications_dir):
        os.makedirs(applications_dir)

    entries = [DESKTOP_GRAPEJUICE, DESKTOP_STUDIO, DESKTOP_PLAYER]
    for entry in entries:
        install_desktop_file(
            os.path.join(variables.application_dir(), "assets", entry),
            applications_dir
        )


def mime_assoc(desktop, mime_type):
    os.spawnlp(os.P_WAIT, "xdg-mime", "xdg-mime", "default", desktop, mime_type)


def update_protocol_handlers():
    mime_assoc(DESKTOP_STUDIO, "x-scheme-handler/roblox-studio")
    mime_assoc(DESKTOP_PLAYER, "x-scheme-handler/roblox-player")


def install_main():
    copy_files()
    install_packages()
    install_desktop_files()
    update_protocol_handlers()


if __name__ == "__main__":
    install_main()
