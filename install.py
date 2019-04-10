#!/usr/bin/env python3

def perform_install():
    import os
    os.execlp("bash", "bash", "./install.sh")


def err_py37():
    import tkinter
    from tkinter import messagebox

    root = tkinter.Tk()
    root.withdraw()

    messagebox.showerror("Out of date",
                         "Your current version of python is out of date and therefore Grapejuice cannot be installer")


def have_py37():
    import sys
    satisfied = sys.version_info >= (3, 7)
    if not satisfied:
        err_py37()

    return satisfied


if __name__ == "__main__":
    if have_py37():
        perform_install()
