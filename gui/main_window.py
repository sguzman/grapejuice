import os

from gi.repository import Gtk

import install
import robloxctrl
import update
import variables
import winectrl
from gui.about_window import AboutWindow
from gui.window_base import WindowBase


class MainWindowHandlers:
    def on_destroy(self, *args):
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
        robloxctrl.run_installer()

    def run_roblox_studio(self, *args):
        if not robloxctrl.run_studio():
            dialog_text = "Roblox Studio could not be launched. You might have to install it first by going to "
            "the Maintanance tab."

            dialog = Gtk.MessageDialog(
                parent=self.window,
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

    def update_desktop_files(self, *args):
        install.install_desktop_files()

    def update_protocol_handlers(self, *args):
        install.update_protocol_handlers()

    def show_about(self, *args):
        about = AboutWindow()
        about.run()

    def install_mime_files(self, *args):
        install.install_mime_files()

    def update_file_assoc(self, *args):
        install.update_file_associations()

    def perform_update(self, *args):
        update.update_and_reopen()

    def reinstall(self, *args):
        update.update_and_reopen()


class MainWindow(WindowBase):
    def __init__(self):
        super().__init__(
            variables.grapejuice_main_glade(),
            MainWindowHandlers
        )

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
            s = "Grapejuice is up to date\n{}".format(str(update.local_version()))
            self.update_status_label().set_text(s)
            self.update_button().hide()

    def window(self):
        return self.builder.get_object("main_window")

    def show(self):
        self.window().show()
