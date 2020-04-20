#!/usr/bin/env python3
import os
import site
import subprocess
import sys

if os.getuid() == 0:
    if "CI_JOB_ID" not in os.environ:
        msg = "Installing Grapejuice as root is not supported"
        print(msg, file=sys.stderr)
        raise RuntimeError(msg)

REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7

K_GRAPEJUICE_INSTALL_PREFIX = "GRAPEJUICE_INSTALL_PREFIX"
K_GRAPEJUICE_IS_PACKAGING = "GRAPEJUICE_IS_PACKAGING"
K_GRAPEJUICE_PACKAGE_PREFIX = "GRAPEJUICE_PACKAGE_PREFIX"


def get_install_prefix():
    if K_GRAPEJUICE_INSTALL_PREFIX in os.environ:
        assert K_GRAPEJUICE_PACKAGE_PREFIX in os.environ, f"{K_GRAPEJUICE_PACKAGE_PREFIX} must be present in the " \
                                                          f"environment for a packaging job to work "

        os.environ[K_GRAPEJUICE_IS_PACKAGING] = "yes"  # Assume we are packaging

        print("! The installation script is assuming that grapejuice is being packaged, file assocations will NOT be "
              "made !")

        return os.getenv(K_GRAPEJUICE_INSTALL_PREFIX)

    here = os.path.dirname(__file__)
    site.addsitedir(os.path.join(here, "src"))

    try:
        from grapejuice_common.variables import dot_local
        return dot_local()
    except ImportError as e:
        raise e


def perform_install():
    os.environ["USED_INSTALL_PY"] = "1"

    install_prefix = get_install_prefix()
    assert os.path.exists(install_prefix), f"The install prefix directory '{install_prefix}' does not exist! Please " \
                                           f"create it if you are absolutely sure this is the right path "

    os.environ[K_GRAPEJUICE_INSTALL_PREFIX] = install_prefix
    print("! Using the install prefix at ", install_prefix)

    if "VIRTUAL_ENV" in os.environ:
        print("! Detected VIRTUAL_ENV, finding system Python interpreter...")
        venv = os.environ["VIRTUAL_ENV"]

        viable_paths = list(filter(lambda p: venv not in p, os.environ["PATH"].split(":")))

        py3 = list(map(lambda s: os.path.join(s, "python3"), viable_paths))
        py37 = list(map(lambda s: os.path.join(s, "python3.7"), viable_paths))

        viable_binaries = list(filter(os.path.exists, py3 + py37))

        def interpreter_is_viable(path):
            ver = subprocess.check_output([
                path,
                "-c",
                "import sys; print(sys.version_info.major, sys.version_info.minor)"
            ]).decode("UTF-8")

            major, minor = list(map(int, ver.split(" ")))

            return major >= REQUIRED_MAJOR and minor >= REQUIRED_MINOR

        viable_interpreters = list(filter(interpreter_is_viable, viable_binaries))

        assert len(viable_interpreters) > 0, "Could not find a valid Python3 interpreter in $PATH"

        python = viable_interpreters[0]
        print("! Using system Python at", python)

        subprocess.check_call(["bash", "install.sh", python])

    else:
        subprocess.check_call(["bash", "install.sh", sys.executable])


def have_tkinter():
    try:
        import tkinter
        return True
    except ImportError:
        return False


def err_tkinter(title, message):
    import tkinter
    from tkinter import messagebox

    root = tkinter.Tk()
    root.withdraw()

    messagebox.showerror(title, message)


def have_zenity():
    import os
    return os.path.exists("/usr/bin/zenity")


def err_zenity(title, message):
    import os

    os.spawnlp(os.P_WAIT, "zenity", "zenity", "--error", title, "--no-wrap", "--text={}".format(message))


def err_desperation(message):
    import os

    os.spawnlp(os.P_WAIT, "xmessage", "xmessage", message)


def show_err(title, message):
    if have_tkinter():
        err_tkinter(title, message)
    elif have_zenity():
        err_zenity(title, message)
    else:
        err_desperation(message)


def err_py37():
    import sys
    show_err("Out of date",
             "Your current version of python is out of date and therefore Grapejuice cannot be installed. Python 3.7 "
             "is required.Check the Grapejuice source repository for new installation instructions.\n\nYou have:\n" + sys.version)


def have_py37():
    import sys

    satisfied = sys.version_info.major >= REQUIRED_MAJOR and sys.version_info.minor >= REQUIRED_MINOR

    if not satisfied:
        err_py37()
        sys.exit(-1)

    return satisfied


if __name__ == "__main__":
    if have_py37():
        perform_install()
