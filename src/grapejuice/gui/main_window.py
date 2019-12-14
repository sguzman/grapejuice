import os

from grapejuice import update, background
from grapejuice.tasks import DisableMimeAssociations, ApplyDLLOverrides, InstallRoblox, DeployAssociations, \
    GraphicsModeOpenGL, SandboxWine
from grapejuice.update import update_and_reopen
from grapejuice_common import variables
from grapejuice_common import winectrl, version
from grapejuice_common.errors import NoWineError
from grapejuice_common.event import Event
from grapejuice_common.window_base import WindowBase

on_destroy = Event()
show_about_event = Event()
close_about_event = Event()

once_task_tracker = dict()


def on_task_removed(task: background.BackgroundTask):
    if task in once_task_tracker.keys():
        once_task_tracker[task] = None


background.tasks.task_removed.add_listener(on_task_removed)


def run_task_once(task_class, on_already_running: callable, *args, **kwargs):
    if task_class in once_task_tracker.values():
        on_already_running()
        return

    task = task_class(*args, **kwargs)
    once_task_tracker[task] = task_class

    background.tasks.add(task)


def dialog(dialog_text):
    from gi.repository import Gtk

    gtk_dialog = Gtk.MessageDialog(
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=dialog_text
    )
    gtk_dialog.run()
    gtk_dialog.destroy()


def generic_already_running():
    dialog("This task is already being performed!")


def xdg_open(*args):
    os.spawnlp(os.P_NOWAIT, "xdg-open", "xdg-open", *args)


class MainWindowHandlers:
    def on_destroy(self, *_):
        from gi.repository import Gtk
        on_destroy()
        Gtk.main_quit()

    def run_winecfg(self, *_):
        winectrl.winecfg()

    def run_regedit(self, *_):
        winectrl.regedit()

    def run_winetricks(self, *_):
        winectrl.wine_tricks()

    def disable_mime_assoc(self, *_):
        run_task_once(DisableMimeAssociations, generic_already_running)

    def sandbox(self, *_):
        run_task_once(SandboxWine, generic_already_running)

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

        run_task_once(InstallRoblox, generic_already_running)

    def run_roblox_studio(self, *_):
        from grapejuice_common.dbus_client import dbus_connection

        if not dbus_connection().launch_studio():
            dialog_text = "Roblox Studio could not be launched. You might have to install it first by going to the " \
                          "Maintanance tab. "

            dialog(dialog_text)

    def wine_explorer(self, *_):
        winectrl.explorer()

    def apply_dll_overrides(self, *_):
        run_task_once(ApplyDLLOverrides, generic_already_running)

    def open_drive_c(self, *_):
        xdg_open(variables.wine_drive_c())

    def show_about(self, *_):
        show_about_event()

    def close_about(self, *_):
        close_about_event()

    def show_wiki(self, *_):
        xdg_open(variables.git_wiki())

    def perform_update(self, *_):
        dialog("If the Grapejuice upgrade breaks your installation, please redo the Grapejuice installation according "
               "to the instructions in the Grapejuice git repository. The upgrade will begin after you close this "
               "dialog.")

        update.update_and_reopen()

    def reinstall(self, *_):
        update_and_reopen()

    def deploy_assocs(self, *_):
        run_task_once(DeployAssociations, generic_already_running)

    def launch_sparklepop(self, *_):
        os.spawnlp(os.P_NOWAIT, "python", "python", "-m", "sparklepop")

    def graphicsmode_opengl(self, *_):
        run_task_once(GraphicsModeOpenGL, generic_already_running)


class MainWindow(WindowBase):
    def __init__(self):
        super().__init__(
            variables.grapejuice_main_glade(),
            MainWindowHandlers
        )
        self._build()

        self.update_status_label().set_text("Checking for updates...")
        self.update_update_status()

        background.tasks.tasks_changed.add_listener(self.on_tasks_changed)
        on_destroy.add_listener(self.before_destroy)
        show_about_event.add_listener(self.show_about)
        close_about_event.add_listener(self.close_about)

        self.on_tasks_changed()

    def update_status_label(self):
        return self.builder.get_object("update_status_label")

    def update_button(self):
        return self.builder.get_object('update_button')

    def update_update_status(self):
        w = self

        class CheckUpdates(background.BackgroundTask):
            def __init__(self):
                super().__init__("Checking for a newer version of Grapejuice")

            def run(self) -> None:
                if version.update_available():
                    s = "This version of Grapejuice is out of date\n{} -> {}".format(
                        str(version.local_version()),
                        str(version.cached_remote_version)
                    )

                    w.update_status_label().set_text(s)
                    w.update_button().show()
                else:
                    local_ver = version.local_version()
                    if local_ver > version.cached_remote_version:
                        s = "This version of Grapejuice is from the future\n{}".format(str(local_ver))
                    else:
                        s = "Grapejuice is up to date\n{}".format(str(local_ver))

                    w.update_status_label().set_text(s)
                    w.update_button().hide()

                self.finish()

        background.tasks.add(CheckUpdates())

    @property
    def window(self):
        return self.builder.get_object("main_window")

    @property
    def background_task_button(self):
        return self.builder.get_object("background_task_button")

    @property
    def background_task_spinner(self):
        return self.builder.get_object("background_task_spinner")

    @property
    def background_task_menu(self):
        return self.builder.get_object("background_task_menu")

    def on_tasks_changed(self):
        if background.tasks.count > 0:
            self.background_task_button.show()
            self.background_task_spinner.start()

        else:
            self.background_task_button.hide()
            self.background_task_menu.hide()
            self.background_task_spinner.stop()

    @property
    def about_window(self):
        return self.builder.get_object("grapejuice_about")

    def show_about(self):
        self.about_window.show()

    def close_about(self):
        self.about_window.hide()

    def show(self):
        self.window.show()

    def before_destroy(self):
        background.tasks.tasks_changed.remove_listener(self.on_tasks_changed)
