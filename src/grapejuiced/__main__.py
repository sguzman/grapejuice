import argparse
import signal
import sys

from grapejuice_common import log_config, self_test
from grapejuice_common.pid_file import PIDFile, daemon_pid_file


def spawn(pid_file: PIDFile):
    from grapejuiced.state import State
    state = State()

    def on_sigint(signum, frame) -> None:
        print("> Responding to SIGINT, stopping...")
        state.stop()

    signal.signal(signal.SIGINT, on_sigint)

    print("> Spawning a new daemon")
    pid_file.write_pid()
    state.start_service()
    state.start()


def func_daemon(*_):
    pid_file = daemon_pid_file()

    if pid_file.is_running():
        print("> Another daemon is already running, quitting...")
        return

    spawn(pid_file)


def func_kill(*_):
    print("> You swing your sword...")

    pid_file = daemon_pid_file()
    if pid_file.is_running():
        print("> Killed daemon with pid {} in one sweeping blow.".format(pid_file.pid))
        pid_file.kill()

    else:
        print("> You swing at the air, because there is no daemon. You take 20 damage as you hit your leg.")


def main(in_args=None):
    log_config.configure_logging("grapejuice-daemon")
    self_test.post.run()

    if in_args is None:
        in_args = sys.argv[1:]

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
    main()
