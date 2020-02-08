import argparse
import os
import sys

from grapejuice_packaging.debian import DebianPlatform
from grapejuice_packaging.packaging_platform import Platform
from grapejuice_packaging.pypi import PyPIPlatform

HERE = os.path.dirname(__file__)
SRC_DIRECTORY = os.path.dirname(HERE)
PROJECT_DIRECTORY = os.path.dirname(SRC_DIRECTORY)

os.chdir(PROJECT_DIRECTORY)


def main(in_args=None):
    if in_args is None:
        in_args = sys.argv

    parser = argparse.ArgumentParser(prog="grapejuice_packaging", description="Package grapejuice")
    subparsers = parser.add_subparsers(title="Distributions")

    parser_debian = subparsers.add_parser("debian")
    parser_debian.set_defaults(platform=DebianPlatform)

    parser_pypi = subparsers.add_parser("pypi")
    parser_pypi.set_defaults(platform=PyPIPlatform)

    args = parser.parse_args(in_args[1:])
    assert hasattr(args, "platform")

    platform: Platform = args.platform()
    return platform.run()


if __name__ == '__main__':
    sys.exit(main())
