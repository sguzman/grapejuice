#!/usr/bin/env python3

import os
import shutil

import grapejuice.deployment as install
import grapejuice_common.variables as variables


def uninstall_desktop_files():
    for entry in os.listdir(variables.desktop_assets_dir()):
        file = os.path.join(variables.xdg_applications_dir(), entry)
        if os.path.exists(file) and os.path.isfile(file):
            os.remove(file)


def uninstall_mime_files():
    for mime in os.listdir(variables.mime_xml_assets_dir()):
        file = os.path.join(variables.xdg_mime_packages(), mime)

        if os.path.exists(file) and os.path.isfile(file):
            os.remove(file)


def remove_application_dir():
    shutil.rmtree(variables.system_application_dir(), ignore_errors=True)


def uninstall_main():
    uninstall_desktop_files()
    uninstall_mime_files()
    install.update_mime_database()
    remove_application_dir()


if __name__ == '__main__':
    uninstall_main()
