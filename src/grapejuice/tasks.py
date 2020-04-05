import os
import subprocess

from dbus import DBusException

from grapejuice import background, deployment
from grapejuice_common import winectrl, robloxctrl, variables
from grapejuice_common.dist_info import dist_info, DistributionType


def install_roblox():
    from grapejuice_common.dbus_client import dbus_connection
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


class DeployAssociations(background.BackgroundTask):
    def __init__(self):
        super().__init__("Deploying associations")

    def run(self) -> None:
        if dist_info.distribution_type == DistributionType.source:
            os.environ[variables.K_GRAPEJUICE_INSTALL_PREFIX] = variables.dot_local()
            deployment.post_install()

        else:
            self._log.error(f"{DeployAssociations.__name__} is only supported on source distributions")

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
        from grapejuice_common.dbus_client import dbus_connection
        dbus_connection().launch_studio()
        self.finish()


class ExtractFastFlags(background.BackgroundTask):
    def __init__(self):
        super().__init__("Extracting Fast Flags")

    def run(self) -> None:
        try:
            from grapejuice_common.dbus_client import dbus_connection
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
