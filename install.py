#!/usr/bin/env python3

def perform_install():
    import sys
    import subprocess

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

    satisfied = sys.version_info.major >= 3 and sys.version_info.minor >= 7

    if not satisfied:
        err_py37()
        sys.exit(-1)

    return satisfied


if __name__ == "__main__":
    if have_py37():
        perform_install()
