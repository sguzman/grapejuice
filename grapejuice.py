import argparse
import os

import robloxctrl


def main_gui():
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    import windows

    main_window = windows.main_window()
    main_window.show_all()
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
        return

    parser.print_help()


if __name__ == "__main__":
    main()
