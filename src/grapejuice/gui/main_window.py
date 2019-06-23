import os

from grapejuice import update, deployment
from grapejuice_common import WindowBase, robloxctrl, winectrl
from grapejuice_common import variables


class MainWindowHandlers:
    def on_destroy(self, *args):
        from gi.repository import Gtk
        Gtk.main_quit()

    def run_winecfg(self, *args):
        winectrl.winecfg()

    def run_regedit(self, *args):
        winectrl.regedit()

    def run_winetricks(self, *args):
        winectrl.wine_tricks()

    def disable_mime_assoc(self, *args):
        winectrl.disable_mime_assoc()

    def sandbox(self, *args):
        winectrl.sandbox()

    def run_roblox_installer(self, *args):
        from grapejuice_common.dbus_client import dbus_connection
        dbus_connection.install_roblox()

    def run_roblox_studio(self, *args):
        from grapejuice_common.dbus_client import dbus_connection
        from gi.repository import Gtk

        if not dbus_connection.launch_studio():
            dialog_text = "Roblox Studio could not be launched. You might have to install it first by going to the " \
                          "Maintanance tab. "

            dialog = Gtk.MessageDialog(
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text=dialog_text
            )
            dialog.run()
            dialog.destroy()

    def wine_explorer(self, *args):
        winectrl.explorer()

    def apply_dll_overrides(self, *args):
        winectrl.load_dll_overrides()

    def open_drive_c(self, *args):
        os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", variables.wine_drive_c())

    def show_about(self, *args):
        import grapejuice.gui as gui
        about = gui.AboutWindow()
        about.run()

    def perform_update(self, *args):
        update.update_and_reopen()

    def reinstall(self, *args):
        update.update_and_reopen()

    def deploy_assocs(self, *args):
        deployment.post_install()

    def launch_sparklepop(self, *args):
        os.spawnlp(os.P_NOWAIT, "python", "python", "-m", "sparklepop")

    def graphicsmode_opengl(self, *args):
        robloxctrl.set_graphics_mode_opengl()


class MainWindow(WindowBase):
    def __init__(self):
        super().__init__(
            variables.grapejuice_main_glade(),
            MainWindowHandlers
        )
        self._build()

        self.update_status_label().set_text("Checking for updates...")
        self.update_update_status()

    def update_status_label(self):
        return self.builder.get_object("update_status_label")

    def update_button(self):
        return self.builder.get_object('update_button')

    def update_update_status(self):
        if update.update_available():
            s = "This version of Grapejuice is out of date\n{} -> {}".format(
                str(update.local_version()),
                str(update.cached_remote_version)
            )

            self.update_status_label().set_text(s)
            self.update_button().show()
        else:
            local_ver = update.local_version()
            if local_ver > update.cached_remote_version:
                s = "This version of Grapejuice is from the future\n{}".format(str(local_ver))
            else:
                s = "Grapejuice is up to date\n{}".format(str(local_ver))

            self.update_status_label().set_text(s)
            self.update_button().hide()

    def window(self):
        return self.builder.get_object("main_window")

    def show(self):
        self.window().show()