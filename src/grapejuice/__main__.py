import sys

from grapejuice._internal import main as main

if __name__ == "__main__":
    sys.argv[0] = "Grapejuice"  # Hope this doesn't break anything
    sys.exit(main(sys.argv))
