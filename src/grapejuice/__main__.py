import argparse
import os
import shutil
import sys

import grapejuice_common.util
import grapejuice_common.variables as variables
from grapejuice_common.dbus_client import dbus_connection


def on_exit():
    p = variables.tmp_path()
    if os.path.exists(p) and os.path.isdir(p):
        shutil.rmtree(variables.tmp_path())


def main_gui():
    sys.argv[0] = "Grapejuice"

    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    from grapejuice.gui.main_window import MainWindow

    main_window = MainWindow()
    main_window.show()
    Gtk.main()


def func_gui(args):
    main_gui()


def func_post_install(args):
    from grapejuice import deployment
    deployment.post_install()


def func_player(args):
    if dbus_connection.play_game(grapejuice_common.util.prepare_uri(args.uri)):
        return 0

    return 1


def func_studio(args):
    uri = grapejuice_common.util.prepare_uri(args.uri)
    if uri:
        is_local = False
        if not uri.startswith("roblox-studio:"):
            uri = "Z:" + uri.replace("/", "\\")
            is_local = True

        if is_local:
            dbus_connection.edit_local_game(uri)
        else:
            dbus_connection.edit_cloud_game(uri)

    else:
        dbus_connection.launch_studio()


def main(in_args):
    parser = argparse.ArgumentParser(prog="grapejuice", description="Manage Roblox on Linux")
    subparsers = parser.add_subparsers(title="subcommands", help="sub-command help")

    parser_gui = subparsers.add_parser("gui")
    parser_gui.set_defaults(func=func_gui)

    parser_post_install = subparsers.add_parser("post_install")
    parser_post_install.set_defaults(func=func_post_install)

    parser_player = subparsers.add_parser("player")
    parser_player.add_argument("uri", type=str, help="Your Roblox token to join a game")
    parser_player.set_defaults(func=func_player)

    parser_studio = subparsers.add_parser("studio")
    parser_studio.add_argument("--uri", type=str, help="The URI or file to open roblox studio with", required=False)
    parser_studio.set_defaults(func=func_studio)

    args = parser.parse_args(in_args[1:])
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()

    return 1


if __name__ == "__main__":
    main(sys.argv)
