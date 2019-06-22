import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

from grapejuice_common.dbus_config import bus_path
from grapejuiced.dbus_service import DBusService


class State:
    def __init__(self):
        DBusGMainLoop(set_as_default=True)

        self.session_bus = dbus.SessionBus()
        self.service = DBusService(self.session_bus, bus_path)
        self.loop = GLib.MainLoop()

    def start(self):
        self.loop.run()
        return self
