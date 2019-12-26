import os
import time

from dbus import DBusException
from packaging import version

import grapejuice_common.dbus_config as dbus_config
from grapejuice_common.pid_file import daemon_pid_file


class DBusConnection:
    def __init__(self, connection_attempts=5, **kwargs):
        import dbus

        if "bus" in kwargs.keys():
            self.bus = kwargs["bus"]

        else:
            self.bus = dbus.SessionBus()

        self.pid_file = daemon_pid_file()
        self.daemon_alive = self.pid_file.is_running()
        self.proxy = None

        if not self.daemon_alive:
            self._spawn_daemon()
            self._wait_for_daemon(5)

        self._try_connect(attempts=connection_attempts)

    @property
    def connected(self):
        return self.proxy is not None

    def _wait_for_daemon(self, attempts: int):
        attempts_remaining = attempts

        while not self.daemon_alive and attempts_remaining > 0:
            attempts_remaining -= 1
            self.daemon_alive = self.pid_file.is_running(remove_junk=False)
            time.sleep(.5)

    def _try_connect(self, attempts: int):
        attempts_remaining = attempts
        while attempts_remaining > 0 and not self.connected:
            attempts_remaining -= 1
            try:
                self.proxy = self.bus.get_object(dbus_config.bus_name, dbus_config.bus_path)

            except DBusException:
                self.daemon_alive = False

            if not self.connected:
                time.sleep(.5)

    def launch_studio(self):
        return self.proxy.LaunchStudio()

    def play_game(self, uri):
        if uri:
            return self.proxy.PlayGame(uri)

        return False

    def edit_local_game(self, place_path):
        return self.proxy.EditLocalGame(place_path)

    def edit_cloud_game(self, uri):
        if uri:
            return self.proxy.EditCloudGame(uri)

        return self.launch_studio()

    def install_roblox(self):
        self.proxy.InstallRoblox()

    def _spawn_daemon(self):
        os.spawnlp(os.P_NOWAIT, "python", "python", "-m", "grapejuiced", "daemonize")

    def version(self):
        return self.proxy.Version()

    def extract_fast_flags(self):
        self.proxy.ExtractFastFlags()

    def wine_version(self):
        return version.parse(self.proxy.WineVersion())


connection = None


def dbus_connection():
    global connection
    if connection is None:
        connection = DBusConnection()

    return connection
