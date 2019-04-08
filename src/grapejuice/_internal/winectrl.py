import os
import shutil
import time

import grapejuice._internal.variables as variables


def prepare():
    prefix_dir = variables.wineprefix_dir()
    os.environ["WINEPREFIX"] = prefix_dir
    os.environ["WINEARCH"] = "win64"

    if not os.path.exists(prefix_dir):
        os.makedirs(prefix_dir)


def winecfg():
    prepare()
    os.spawnlp(os.P_NOWAIT, "wine", "wine", "winecfg")


def regedit():
    prepare()
    os.spawnlp(os.P_NOWAIT, "wine", "wine", "regedit")


def explorer():
    prepare()
    os.spawnlp(os.P_NOWAIT, "wine", "wine", "explorer")


def load_reg(srcfile):
    prepare()
    target_filename = str(int(time.time())) + ".reg"
    target_path = os.path.join(variables.wine_temp(), target_filename)
    shutil.copyfile(srcfile, target_path)

    winreg = "C:\\windows\\temp\\{}".format(target_filename)
    os.spawnlp(os.P_WAIT, "wine", "wine", "regedit", "/S", winreg)
    os.spawnlp(os.P_WAIT, "wine64", "wine64", "regedit", "/S", winreg)

    os.remove(target_path)


def wine_tricks():
    prepare()
    os.spawnlp(os.P_NOWAIT, "winetricks", "winetricks")


def disable_mime_assoc():
    load_reg(os.path.join(variables.assets_dir(), "disable_mime_assoc.reg"))


def load_dll_overrides():
    load_reg(os.path.join(variables.assets_dir(), "dll_overrides.reg"))


def sandbox():
    user_dir = variables.wine_user()
    if os.path.exists(user_dir) and os.path.isdir(user_dir):
        for dir in os.listdir(user_dir):
            p = os.path.join(user_dir, dir)
            if os.path.islink(p):
                os.remove(p)


def create_prefix():
    disable_mime_assoc()
    sandbox()
    load_dll_overrides()


def prefix_exists():
    return os.path.exists(variables.wineprefix_dir())


def run_exe(exe_path, *args):
    prepare()
    if len(args) > 0:
        os.spawnlp(os.P_NOWAIT, "wine", "wine", exe_path, *args)
    else:
        os.spawnlp(os.P_NOWAIT, "wine", "wine", exe_path)
