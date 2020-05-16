import argparse
import os
import sys

from grapejuice_packaging.builders.linux_package_builder import LinuxPackageBuilder


def func_linux_package(args):
    build_dir = os.path.join(".", "build", "linux_package") if args.build_dir is None else args.build_dir
    dist_dir = os.path.join(".", "dist", "linux_package") if args.dist_dir is None else args.dist_dir

    builder = LinuxPackageBuilder(build_dir, dist_dir)

    builder.build()


def main(in_args=None):
    if in_args is None:
        in_args = sys.argv

    parser = argparse.ArgumentParser(prog="grapejuice", description="Manage Roblox on Linux")
    subparsers = parser.add_subparsers(title="subcommands", help="sub-command help")

    parser_linux_package = subparsers.add_parser("linux_package")
    parser_linux_package.add_argument("--build-dir", required=False)
    parser_linux_package.add_argument("--dist-dir", required=False)
    parser_linux_package.set_defaults(func=func_linux_package)

    args = parser.parse_args(in_args[1:])

    if hasattr(args, "func"):
        f: callable = args.func
        return f(args) or 0

    else:
        parser.print_help()

    return 1


if __name__ == '__main__':
    sys.exit(main())
