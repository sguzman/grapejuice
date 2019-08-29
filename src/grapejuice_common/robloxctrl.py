import os
import re

import wget

import grapejuice_common.variables as variables
import grapejuice_common.winectrl as winectrl

DOWNLOAD_URL = "https://www.roblox.com/install/setup.ashx"


def set_graphics_mode(mode: int):
    settings_path = variables.wine_roblox_global_settings_13()
    if not os.path.exists(settings_path):
        return False

    ptn = r'token name=\"GraphicsMode\">(\d+)</token'
    gl = 'token name="GraphicsMode">' + str(mode) + '</token'

    output_lines = []
    with open(settings_path, "r") as fp:
        for line in fp.readlines():
            if "GraphicsMode" in line:
                line = re.sub(ptn, gl, line)

            output_lines.append(line)

    with open(settings_path, "w") as fp:
        fp.writelines(output_lines)


def set_graphics_mode_opengl():
    set_graphics_mode(4)


def get_installer():
    install_path = variables.installer_path()

    if os.path.exists(install_path):
        os.remove(install_path)

    wget.download(DOWNLOAD_URL, install_path)


def run_installer():
    winectrl.create_prefix()
    get_installer()
    winectrl.run_exe(variables.installer_path())


def locate_in_versions(exe_name):
    versions = os.path.join(variables.wine_roblox_prog(), "Versions")
    if not os.path.exists(versions):
        return None

    for dir in os.listdir(versions):
        fp = os.path.join(versions, dir)
        if os.path.isdir(fp):
            lp = os.path.join(fp, exe_name)
            if os.path.exists(lp) and os.path.isfile(lp):
                return lp


def locate_studio_launcher():
    exe_name = "RobloxStudioLauncherBeta.exe"
    versioned_launcher = locate_in_versions(exe_name)
    if not versioned_launcher:
        launcher = os.path.join(variables.wine_roblox_prog(), "Versions", exe_name)
        if os.path.exists(launcher):
            return launcher

    return versioned_launcher


def locate_player_launcher():
    return locate_in_versions("RobloxPlayerLauncher.exe")


def run_studio(uri="", ide=False):
    launcher = locate_studio_launcher()
    if launcher is None:
        return False

    if ide:
        winectrl.run_exe_nowait(launcher, "-ide", uri)
    else:
        if uri:
            winectrl.run_exe_nowait(launcher, uri)
        else:
            winectrl.run_exe_nowait(launcher, "-ide")

    return True


def run_player(uri):
    player = locate_player_launcher()
    if player is None:
        return False

    winectrl.run_exe_nowait(player, uri)
    return True
