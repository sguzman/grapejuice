import atexit
import os
import re
import signal

import psutil


class EmptyPIDError(RuntimeError):
    def __init__(self, path):
        super().__init__("Got empty string from PID file " + path)


class AlreadyRunningError(RuntimeError):
    pass


class PIDFile:
    def __init__(self, name: str):
        self._name = re.sub(r"(\W)", "_", name)

        if "XDG_RUNTIME_DIR" in os.environ:
            self._path = os.path.join(os.environ["XDG_RUNTIME_DIR"], self._name + ".pid")

        else:
            self._path = os.path.join("/tmp", self._name + ".pid")

        self._wrote_pid = False

        atexit.register(self._at_exit)

    def _at_exit(self, *_):
        if self._wrote_pid:
            os.remove(self._path)

    def exists(self):
        return os.path.exists(self._path)

    @property
    def pid(self):
        with open(self._path, "r") as fp:
            s = fp.read().strip()
            if not s:
                raise EmptyPIDError(self._path)

            return int(s)

    def _remove_file(self):
        if os.path.exists(self._path):
            os.remove(self._path)

    def is_running(self, remove_junk=True):
        if not self.exists():
            return False

        try:
            process = psutil.Process(pid=self.pid)
            return process.is_running()

        except psutil.NoSuchProcess:
            if remove_junk:
                self._remove_file()

            return False

    def write_pid(self):
        try:
            if self.is_running():
                raise AlreadyRunningError

        except EmptyPIDError:
            pass

        with open(self._path, "w+") as fp:
            fp.write(str(os.getpid()))

        self._wrote_pid = True

    def kill(self):
        if self.is_running():
            os.kill(self.pid, signal.SIGINT)


def daemon_pid_file():
    return PIDFile("grapejuiced")
