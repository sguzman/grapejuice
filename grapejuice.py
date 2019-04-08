import argparse
import atexit
import os
import shutil

import robloxctrl
import variables


def on_exit():
    p = variables.tmp_path()
    if os.path.exists(p) and os.path.isdir(p):
        shutil.rmtree(variables.tmp_path())


def main_gui():
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
    from gui import MainWindow

    main_window = MainWindow()
    main_window.show()
    Gtk.main()


def main_cli():
    pass


def main():
    parser = argparse.ArgumentParser(description="Manage Roblox on Linux")

    parser.add_argument("--gui", help="Run Grapejuice in GUI mode", action="store_true")
    parser.add_argument("--player", help="Run Roblox Player", action="store_true")
    parser.add_argument("--studio", help="Run Roblox Studio", action="store_true")
    parser.add_argument("--uri", help="A Roblox URI", required=False)

    args = parser.parse_args()

    def get_uri():
        if args.uri is not None and args.uri:
            return args.uri.replace("'", "")

        return None

    if args.studio:
        uri = get_uri()
        if uri is None:
            print("Please supply a URI")
            return

        ide = False
        if not uri.startswith("roblox-studio"):
            uri = "Z:" + uri.replace("/", "\\")
            ide = True

        robloxctrl.run_studio(uri, ide)
        return

    if args.player:
        uri = get_uri()
        if uri is None:
            os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", "https://roblox.com/games")
            return

        robloxctrl.run_player(uri)
        return

    if args.gui:
        main_gui()
        atexit.register(on_exit)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
