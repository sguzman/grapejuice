import os
import sys


def home():
    return os.environ["HOME"]


def application_dir():
    return os.path.join(home(), ".local", "share", "grapejuice")


def run_script_path():
    return os.path.join(application_dir(), "bin", "grapejuice")


def assets_dir():
    src_assets = os.path.join(src_dir(), "assets")
    if os.path.exists(src_assets):
        return os.path.abspath(src_assets)

    cwd_assets = os.path.join(os.getcwd(), "assets")
    if os.path.exists(cwd_assets):
        return os.path.abspath(cwd_assets)

    app_assets = os.path.join(application_dir(), "assets")
    if os.path.exists(app_assets):
        return os.path.abspath(app_assets)


def src_dir():
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def grapejuice_main_glade():
    return os.path.join(assets_dir(), "grapejuice_main.glade")


def src_init_py():
    current = os.path.join(src_dir(), "__init__.py")
    if os.path.exists(current):
        return current

    current = os.path.join(src_dir(), "src", "grapejuice", "__init__.py")
    if os.path.exists(current):
        return current


def wineprefix_dir():
    return os.path.join(application_dir(), "wineprefix")


def wine_drive_c():
    return os.path.join(wineprefix_dir(), "drive_c")


def wine_roblox_prog():
    return os.path.join(wine_drive_c(), "Program Files (x86)", "Roblox")


def wine_temp():
    p = os.path.join(wine_drive_c(), "windows", "temp")
    if not os.path.exists(p):
        os.makedirs(p)

    return p


def wine_user():
    return os.path.join(wine_drive_c(), "users", os.environ["USER"])


def installer_path():
    return os.path.join(wine_temp(), "Roblox_Installer.exe")


def xdg_applications_dir():
    return os.path.join(home(), ".local", "share", "applications")


def xdg_mime_dir():
    return os.path.join(home(), ".local", "share", "mime")


def xdg_mime_packages():
    return os.path.join(xdg_mime_dir(), "packages")


def git_repository():
    return "https://gitlab.com/brinkervii/grapejuice"


def git_init_py_url():
    return git_repository() + "/raw/master/__init__.py"


def git_zip_download():
    return git_repository() + "/-/archive/master/grapejuice-master.zip"


def tmp_path():
    d = "grapejuice-{}".format(os.getpid())
    p = os.path.join("/tmp", d)

    if not os.path.exists(p):
        os.makedirs(p)
    else:
        if not os.path.isdir(p):
            os.remove(p)
            os.makedirs(p)

    return p


def tmp_zip_path():
    return os.path.join(tmp_path(), "grapejuice-download.zip")
