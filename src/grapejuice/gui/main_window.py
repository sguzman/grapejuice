import os

from grapejuice import update, deployment
from grapejuice_common import WindowBase, robloxctrl, winectrl, version
from grapejuice_common import variables
from grapejuice_common.errors import NoWineError


def dialog(dialog_text):
    from gi.repository import Gtk

    gtk_dialog = Gtk.MessageDialog(
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=dialog_text
    )
    gtk_dialog.run()
    gtk_dialog.destroy()


def install_roblox():
    from grapejuice_common.dbus_client import dbus_connection
    dbus_connection().install_roblox()


def xdg_open(*args):
    os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", *args)


class MainWindowHandlers:
    def on_destroy(self, *_):
        from gi.repository import Gtk
        Gtk.main_quit()

    def run_winecfg(self, *_):
        winectrl.winecfg()

    def run_regedit(self, *_):
        winectrl.regedit()

    def run_winetricks(self, *_):
        winectrl.wine_tricks()

    def disable_mime_assoc(self, *_):
        winectrl.disable_mime_assoc()

    def sandbox(self, *_):
        winectrl.sandbox()

    def run_roblox_installer(self, *_):
        def no_wine_dialog() -> None:
            dialog("Grapejuice could not find a working Wine binary, please install Wine using your operating "
                   "system's package manager in order to install and use Roblox.")

            return None

        try:
            wine_bin = variables.wine_binary()
            if not os.path.exists(wine_bin):
                return no_wine_dialog()

        except NoWineError:
            return no_wine_dialog()

        install_roblox()

    def run_roblox_studio(self, *_):
        from grapejuice_common.dbus_client import dbus_connection

        if not dbus_connection().launch_studio():
            dialog_text = "Roblox Studio could not be launched. You might have to install it first by going to the " \
                          "Maintanance tab. "

            dialog(dialog_text)

    def wine_explorer(self, *_):
        winectrl.explorer()

    def apply_dll_overrides(self, *_):
        winectrl.load_dll_overrides()

    def open_drive_c(self, *_):
        xdg_open(variables.wine_drive_c())

    def show_about(self, *_):
        import grapejuice.gui as gui
        about = gui.AboutWindow()
        about.run()

    def show_wiki(self, *_):
        xdg_open(variables.git_wiki())

    def perform_update(self, *_):
        dialog("If the Grapejuice upgrade breaks your installation, please redo the Grapejuice installation according "
               "to the instructions in the Grapejuice git repository. The upgrade will begin after you close this "
               "dialog.")

        update.update_and_reopen()

    def reinstall(self, *_):
        update.update_and_reopen()

    def deploy_assocs(self, *_):
        deployment.post_install()

    def launch_sparklepop(self, *_):
        os.spawnlp(os.P_NOWAIT, "python", "python", "-m", "sparklepop")

    def graphicsmode_opengl(self, *_):
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
        if version.update_available():
            s = "This version of Grapejuice is out of date\n{} -> {}".format(
                str(version.local_version()),
                str(version.cached_remote_version)
            )

            self.update_status_label().set_text(s)
            self.update_button().show()
        else:
            local_ver = version.local_version()
            if local_ver > version.cached_remote_version:
                s = "This version of Grapejuice is from the future\n{}".format(str(local_ver))
            else:
                s = "Grapejuice is up to date\n{}".format(str(local_ver))

            self.update_status_label().set_text(s)
            self.update_button().hide()

    def window(self):
        return self.builder.get_object("main_window")

    def show(self):
        self.window().show()
