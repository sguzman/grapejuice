import os


def home():
    return os.environ["HOME"]


def application_dir():
    return os.path.join(home(), ".local", "share", "grapejuice")


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
