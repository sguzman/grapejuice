import os
import subprocess

from packaging import version

from grapejuice_common.errors import NoWineError

HERE = os.path.abspath(os.path.dirname(__file__))


def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

    return p


def home():
    return os.environ["HOME"]


def application_dir():
    return os.path.join(xdg_data_home(), "grapejuice")


def assets_dir():
    search_locations = [
        os.path.join(HERE, "assets"),
        os.path.join(src_dir(), "assets"),
        os.path.join(os.getcwd(), "assets"),
        os.path.join(application_dir(), "assets")
    ]

    for p in search_locations:
        if os.path.exists(p):
            return p


def src_dir():
    return os.path.abspath(os.path.dirname(HERE))


def glade_dir():
    return os.path.join(assets_dir(), "glade")


def grapejuice_glade():
    return os.path.join(glade_dir(), "grapejuice.glade")


def about_glade():
    return os.path.join(glade_dir(), "about.glade")


def fast_flag_editor_glade():
    return os.path.join(glade_dir(), "fast_flag_editor.glade")


def grapejuice_components_glade():
    return os.path.join(glade_dir(), "grapejuice_components.glade")


def fast_flag_warning_glade():
    return os.path.join(glade_dir(), "fast_flag_warning.glade")


def sparklepop_glade():
    return os.path.join(glade_dir(), "sparklepop.glade")


def config_base_dir():
    return ensure_dir(os.path.join(xdg_config_home(), "brinkervii"))


def sparklepop_config_dir():
    return ensure_dir(os.path.join(config_base_dir(), "sparklepop"))


def grapejuice_config_dir():
    return ensure_dir(os.path.join(config_base_dir(), "grapejuice"))


def grapejuice_user_settings():
    return os.path.join(grapejuice_config_dir(), "user_settings.json")


def sparklepop_snapshots_dir():
    return ensure_dir(os.path.join(sparklepop_config_dir(), "snapshots"))


def src_init_py():
    search_locations = [
        os.path.join(src_dir(), "grapejuice", "__init__.py"),
        os.path.join(src_dir(), "__init__.py"),
        os.path.join(src_dir(), "src", "grapejuice", "__init__.py")
    ]

    for p in search_locations:
        if os.path.exists(p):
            return p


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


def wine_roblox_appdata():
    return os.path.join(wine_user(), "Local Settings", "Application Data", "Roblox")


def wine_roblox_global_settings_13():
    return os.path.join(wine_roblox_appdata(), "GlobalSettings_13.xml")


def wine_roblox_studio_app_settings():
    return os.path.join(wine_roblox_appdata(), "ClientSettings", "StudioAppSettings.json")


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


def git_wiki():
    return git_repository() + "/-/wikis/home"


def git_init_py_url():
    return git_repository() + "/raw/master/src/grapejuice/__init__.py"


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


def wine_binary(arch=""):
    path_search = []
    if "PATH" in os.environ:
        for spec in os.environ["PATH"].split(":"):
            path_search.append(os.path.join(spec, "wine" + arch))

    static_search = [
        "/opt/wine-stable/bin/wine" + arch,
        "/opt/wine-staging/bin/wine" + arch
    ]

    for p in (path_search + static_search):
        if os.path.exists(p):
            return p

    raise NoWineError()


def wine_binary_64():
    return wine_binary("64")


def required_wine_version():
    return version.parse("wine-4.0.0")
