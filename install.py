#!/usr/bin/env python3
import os
import subprocess
import sys

if os.getuid() == 0:
    if "CI_JOB_ID" not in os.environ:
        msg = "Installing Grapejuice as root is not supported"
        print(msg, file=sys.stderr)
        raise RuntimeError(msg)

REQUIRED_MAJOR = 3
REQUIRED_MINOR = 7


def find_python_interpreter():
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

        return python

    return "python3"


def perform_install():
    subprocess.check_call([find_python_interpreter(), "setup.py", "install_locally"])


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
    subprocess.call(["zenity", "--error", title, "--no-wrap", "--text={}".format(message)])


def err_desperation(message):
    subprocess.call(["xmessage", message])


def show_err(title, message):
    if have_tkinter():
        err_tkinter(title, message)

    elif have_zenity():
        err_zenity(title, message)

    else:
        err_desperation(message)


def err_py37():
    import sys

    ver = f"{REQUIRED_MAJOR}.{REQUIRED_MINOR}"

    show_err("Out of date",
             f"Your current version of python is out of date and therefore Grapejuice cannot be installed.\n\n"
             f"Python {ver} is required. Check the Grapejuice source repository for the installation instructions.\n\n"
             f"You have:\n{sys.version}"
             )


def have_py37():
    import sys

    satisfied = sys.version_info.major >= REQUIRED_MAJOR and sys.version_info.minor >= REQUIRED_MINOR

    if not satisfied:
        exit_code = -1

        try:
            err_py37()

        except Exception as e:
            exit_code = -2
            print(e, file=sys.stderr)

        sys.exit(exit_code)

    return satisfied


if __name__ == "__main__":
    if have_py37():
        perform_install()
