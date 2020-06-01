import os

HERE = os.path.dirname(os.path.abspath(__file__))


def bin_grapejuice_path():
    return os.path.join(HERE, "bin", "grapejuice")


def bin_grapejuiced_path():
    return os.path.join(HERE, "bin", "grapejuiced")


def app_image_app_run():
    return os.path.join(HERE, "appimage", "AppRun")


def app_image_desktop():
    return os.path.join(HERE, "appimage", "grapejuice.desktop")


def app_image_tool():  # Gross
    return os.path.join(HERE, "appimage", "appimagetool-x86_64.AppImage")
