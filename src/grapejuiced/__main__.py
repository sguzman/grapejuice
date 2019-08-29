import argparse
import sys


def func_daemon(args):
    from grapejuiced.state import State
    state = State()
    do_start = False

    print("> Checking for an existing daemon....")
    from grapejuice_common.dbus_client import DBusConnection
    from grapejuiced.__init__ import __version__
    import packaging.version as version
    con = DBusConnection(no_spawn=True, bus=state.session_bus)

    if con.daemon_alive:
        print("> Connected to a daemon")

        con_version = version.parse(con.version())
        my_version = version.parse(__version__)

        if con_version < my_version:
            print("> Terminating an older daemon")
            con.terminate()
            do_start = True

        else:
            print("> Starting a new daemon is not required")

    else:
        do_start = True

    if do_start:
        print("> Spawning a new daemon")
        state.start_service()
        state.start()

    else:
        print("> A new daemon is not required, quitting...")


def func_kill(args):
    print("> Connecting to the Grapejuice daemon")
    from grapejuice_common.dbus_client import DBusConnection
    con = DBusConnection(no_spawn=True)
    if con.daemon_alive:
        con.terminate()

    else:
        print("There is no Grapejuice daemon to kill")


def main(in_args):
    parser = argparse.ArgumentParser(prog="grapejuiced", description="The Grapejuice daemon")
    subparsers = parser.add_subparsers(title="subcommands", help="sub-command help")

    parser_kill = subparsers.add_parser("kill")
    parser_kill.set_defaults(func=func_kill)

    parser_daemon = subparsers.add_parser("daemonize")
    parser_daemon.set_defaults(func=func_daemon)

    args = parser.parse_args(in_args)
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main(sys.argv[1:])
