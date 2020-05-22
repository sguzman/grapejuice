import logging
import os
import subprocess
import sys

from dbus import DBusException

from grapejuice import background
from grapejuice_common import winectrl, robloxctrl, variables
from grapejuice_common.updates.update_provider import UpdateProvider


def install_roblox():
    from grapejuice_common.ipc.dbus_client import dbus_connection
    dbus_connection().install_roblox()


class DisableMimeAssociations(background.BackgroundTask):
    def __init__(self):
        super().__init__("Disabling Wine associations")

    def run(self) -> None:
        winectrl.disable_mime_assoc()
        self.finish()


class ApplyDLLOverrides(background.BackgroundTask):
    def __init__(self):
        super().__init__("Applying DLL overrides")

    def run(self) -> None:
        winectrl.load_dll_overrides()
        self.finish()


class InstallRoblox(background.BackgroundTask):
    def __init__(self):
        super().__init__("Installing Roblox")

    def run(self) -> None:
        try:
            install_roblox()
        except DBusException:
            pass  # TODO: find a proper fix

        self.finish()


class GraphicsModeOpenGL(background.BackgroundTask):
    def __init__(self):
        super().__init__("Changing the Roblox GraphicsMode to OpenGL")

    def run(self) -> None:
        robloxctrl.set_graphics_mode_opengl()
        self.finish()


class SandboxWine(background.BackgroundTask):
    def __init__(self):
        super().__init__("Sandboxing the Wine prefix")

    def run(self) -> None:
        winectrl.sandbox()
        self.finish()


class RunRobloxStudio(background.BackgroundTask):
    def __init__(self):
        super().__init__("Launching Roblox Studio")

    def run(self) -> None:
        from grapejuice_common.ipc.dbus_client import dbus_connection
        dbus_connection().launch_studio()
        self.finish()


class ExtractFastFlags(background.BackgroundTask):
    def __init__(self):
        super().__init__("Extracting Fast Flags")

    def run(self) -> None:
        try:
            from grapejuice_common.ipc.dbus_client import dbus_connection
            dbus_connection().extract_fast_flags()

        except DBusException:
            pass

        self.finish()


class OpenLogsDirectory(background.BackgroundTask):
    def __init__(self):
        super().__init__("Opening logs directory")

    def run(self) -> None:
        path = variables.logging_directory()
        os.makedirs(path, exist_ok=True)

        subprocess.check_call(["xdg-open", path])
        self.finish()


class PerformUpdate(background.BackgroundTask):
    def __init__(self, update_provider: UpdateProvider, reopen: bool = False):
        super().__init__()
        self._update_provider = update_provider
        self._reopen = reopen

    def run(self) -> None:
        log = logging.getLogger(self.__class__.__name__)

        try:
            self._update_provider.do_update()

        except Exception as e:
            log.error(e)

        if self._reopen:
            subprocess.Popen(["bash", "-c", "python3 -m grapejuice gui & disown"], preexec_fn=os.setpgrp)

            from gi.repository import Gtk
            Gtk.main_quit()

            sys.exit(0)

        self.finish()
