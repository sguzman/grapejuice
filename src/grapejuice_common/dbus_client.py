import os
import time

from dbus import DBusException

import grapejuice_common.dbus_config as dbus_config


class DBusConnection:
    def __init__(self):
        import dbus

        self.daemon_alive = False
        self.bus = dbus.SessionBus()
        self._try_connect()
        if not self.daemon_alive:
            self._spawn_daemon()
            self._try_connect(50)

    def _try_connect(self, attempts=1):
        attempts_remaining = attempts
        while attempts_remaining > 0 and not self.daemon_alive:
            attempts_remaining -= 1
            try:
                self.proxy = self.bus.get_object(dbus_config.bus_name, dbus_config.bus_path)
                self.daemon_alive = True
            except DBusException:
                self.daemon_alive = False
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
        os.spawnlp(os.P_NOWAIT, "python", "python", "-m", "grapejuiced")


dbus_connection = DBusConnection()
