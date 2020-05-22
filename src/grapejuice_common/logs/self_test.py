import logging
import os

# Note about the self-test:
# Since part of the self-test is importing all project dependencies, Gtk gets imported.
# Gtk will cache sys.argv[0] and use this to display in the activities window.
# SO VERY IMPORTANT: MAKE SURE sys.arg[0] is hacked BEFORE Gtk is imported!
from grapejuice_common.util.task_sequence import TaskSequence, TaskError

post = TaskSequence("Power On Self Test")


@post.task("Read OS information")
def read_os_release(log: logging.Logger):
    os_release_path = "/etc/os-release"

    if not os.path.exists(os_release_path):
        raise TaskError(f"OS release information does not exist at '{os_release_path}'", can_continue=True)

    log.info(f"-- Path is {os_release_path}")
    with open(os_release_path, "r") as fp:
        for line in fp.readlines():
            log.info(line.strip())


@post.task("Test for root user")
def test_for_root_user(log: logging.Logger):
    if os.getuid() == 0:
        if "CI_JOB_ID" not in os.environ:
            msg = "Running Grapejuice as root is not supported"
            log.error(msg)
            raise TaskError(msg, can_continue=False)


@post.task("Check python dependencies")
def check_python_dependencies(log: logging.Logger):
    def import_psutil():
        import psutil

        return psutil

    def import_py_g_object():
        import gi
        gi.require_version("Gtk", "3.0")

        from gi.repository import Gtk
        from gi.repository import GObject
        from gi.repository import GLib

        return gi, Gtk, GObject, GLib

    def import_packaging():
        import packaging

        return packaging

    def import_requests():
        import requests

        return requests

    def import_wheel():
        import wheel

        return wheel

    def import_setuptools():
        import setuptools

        return setuptools

    def import_dbus():
        import dbus

        return dbus

    def try_import(import_func: callable):
        try:
            import_result = func()
            if isinstance(import_result, tuple):
                results = list(import_result)

            else:
                results = [import_result]

            log.info(f"Import function '{import_func.__name__}' loaded {len(results)} imports")

        except ImportError as e:
            msg = f"Import function '{import_func.__name__}' could not perform the imports it had to. " \
                  f"This installation of grapejuice is incorrect and should be rectified by doing a proper " \
                  f"installation. The underlying error is:\n {str(e)}"

            raise TaskError(msg, can_continue=False)

    map_23 = [
        import_psutil,
        import_py_g_object,
        import_packaging,
        import_requests,
        import_wheel,
        import_setuptools,
        import_dbus
    ]

    for func in map_23:
        try_import(func)
