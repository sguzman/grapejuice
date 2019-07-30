import dbus.service

from grapejuice_common.dbus_config import bus_name


class DBusService(dbus.service.Object):
    def __init__(self, bus, path):
        super().__init__(bus, path, dbus.service.BusName(bus_name))

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="s",
        out_signature="b"
    )
    def EditLocalGame(self, path):
        from grapejuice_common import robloxctrl

        return robloxctrl.run_studio(path, True)

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="s",
        out_signature="b"
    )
    def EditCloudGame(self, uri):
        from grapejuice_common import robloxctrl
        return robloxctrl.run_studio(uri)

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="",
        out_signature="b"
    )
    def LaunchStudio(self):
        from grapejuice_common import robloxctrl
        return robloxctrl.run_studio()

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="s",
        out_signature=""
    )
    def PlayGame(self, uri):
        from grapejuice_common import robloxctrl
        robloxctrl.run_player(uri)

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="",
        out_signature=""
    )
    def InstallRoblox(self):
        from grapejuice_common import robloxctrl
        robloxctrl.run_installer()

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="",
        out_signature=""
    )
    def Terminate(self):
        import sys
        sys.exit(0)

    @dbus.service.method(
        dbus_interface=bus_name,
        in_signature="",
        out_signature="s"
    )
    def Version(self):
        from grapejuice_common import version
        return str(version.local_version())
