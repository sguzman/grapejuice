import inspect
import os


def home():
    return os.environ["HOME"]


def application_dir():
    return os.path.join(home(), ".local", "share", "grapejuice")


def assets_dir():
    return os.path.join(src_dir(), "assets")


def src_dir():
    return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def grapejuice_main_glade():
    return os.path.join(assets_dir(), "grapejuice_main.glade")


def src_init_py():
    return os.path.join(src_dir(), "__init__.py")


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
    return "https://gitlab.com/brinkervii/grapejuice/"


def git_init_py_url():
    return git_repository() + "raw/master/__init__.py"
