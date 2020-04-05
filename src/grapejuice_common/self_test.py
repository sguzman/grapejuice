import logging
import os
from typing import List, Tuple


# Note about the self-test:
# Since part of the self-test is importing all project dependencies, Gtk gets imported.
# Gtk will cache sys.argv[0] and use this to display in the activities window.
# SO VERY IMPORTANT: MAKE SURE sys.arg[0] is hacked BEFORE Gtk is imported!

class TaskError(RuntimeError):
    def __init__(self, message: str, can_continue: bool = True):
        super().__init__(message)
        self._can_continue = can_continue

    @property
    def can_continue(self) -> bool:
        return self._can_continue


class TaskSequence:
    _ok_str = "Y"
    _fail_str = "N"
    _pending_str = "?"

    def __init__(self, name: str):
        self._name = name
        self._log = logging.getLogger(self._name)
        self._tasks: List[Tuple[str, callable]] = []
        self._results: List[str] = []
        self._reset_results()

    def task(self, name: str):
        tasks = self._tasks

        def wrap_function(func: callable):
            tasks.append((name, func))

            def wrapper():
                return func()

            return wrapper

        return wrap_function

    def _reset_results(self):
        self._results = ["?" for _ in self._tasks]

    def _log_results(self):
        self._log.info("Task status: " + "".join(self._results))

    def run(self):
        self._log.info("Running task sequence")
        self._reset_results()
        self._log_results()

        task_counter = 0
        for task_name, task_func in self._tasks:
            self._log.info(f"-- Running task -> {task_name} --")

            try:
                task_func(self._log)
                self._results[task_counter] = self._ok_str

            except TaskError as e:
                self._log.error(str(e))
                self._results[task_counter] = self._fail_str

                if e.can_continue:
                    self._log.warning(f"Task '{task_name}' failed, but we can continue")

                else:
                    self._log.error(f"Aborting due to failed task '{task_name}'")
                    raise e

            self._log.info(f"-- End of task --")

            task_counter += 1
            self._log_results()

        self._log.info(f"{self._name} OK")


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
