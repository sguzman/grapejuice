import os
import subprocess
import sys


def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

    return p


def home():
    return os.environ["HOME"]


def application_dir():
    return os.path.join(xdg_data_home(), "grapejuice")


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


def glade_dir():
    return os.path.join(assets_dir(), "glade")


def grapejuice_main_glade():
    return os.path.join(glade_dir(), "grapejuice_main.glade")


def sparklepop_glade():
    return os.path.join(glade_dir(), "sparklepop.glade")


def config_base_dir():
    return ensure_dir(os.path.join(xdg_config_home(), "brinkervii"))


def sparklepop_config_dir():
    return ensure_dir(os.path.join(config_base_dir(), "sparklepop"))


def grapejuice_config_dir():
    return ensure_dir(os.path.join(config_base_dir(), "grapejuice"))


def sparklepop_snapshots_dir():
    return ensure_dir(os.path.join(sparklepop_config_dir(), "snapshots"))


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
    return ensure_dir(os.path.join(wine_drive_c(), "windows", "temp"))


def wine_user():
    return os.path.join(wine_drive_c(), "users", os.environ["USER"])


def installer_path():
    return os.path.join(wine_temp(), "Roblox_Installer.exe")


def xdg_applications_dir():
    return os.path.join(xdg_data_home(), "applications")


def xdg_mime_dir():
    return os.path.join(xdg_data_home(), "mime")


def xdg_mime_packages():
    return os.path.join(xdg_mime_dir(), "packages")


def xdg_config_home():
    if "XDG_CONFIG_HOME" in os.environ:
        config_home = os.environ["XDG_CONFIG_HOME"]
        if config_home and os.path.exists(config_home) and os.path.isdir(config_home):
            return config_home

    config_home = os.path.join(home(), ".config")
    if not os.path.exists(config_home):
        os.makedirs(config_home)

    return config_home


def xdg_data_home():
    if "XDG_DATA_HOME" in os.environ:
        data_home = os.environ["XDG_DATA_HOME"]
        if data_home and os.path.exists(data_home) and os.path.isdir(data_home):
            return data_home

    data_home = os.path.join(home(), ".local", "share")
    if not os.path.exists(data_home):
        os.makedirs(data_home)

    return data_home


def xdg_documents():
    run = subprocess.run(["xdg-user-dir", "DOCUMENTS"], stdout=subprocess.PIPE)
    documents_path = run.stdout.decode("utf-8").rstrip()

    if os.path.exists(documents_path):
        return documents_path

    documents_path = os.path.join(home(), "Documents")
    return ensure_dir(documents_path)


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
