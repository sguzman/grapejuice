from grapejuice_common import variables
from grapejuice_common.gtk.gtk_stuff import WindowBase
from grapejuice_common.settings import settings


class FastFlagWarning(WindowBase):
    def __init__(self, callback):
        super().__init__(variables.fast_flag_warning_glade(), self)

        self._do_continue = False
        self._callback = callback

        self.devforum_link.set_label("Read more on the Roblox Developer forum")
        self.warn_check.set_active(settings.show_fast_flag_warning)

    @property
    def window(self):
        return self.builder.get_object("fast_flag_warning")

    @property
    def devforum_link(self):
        return self.builder.get_object("devforum_link")

    @property
    def warn_check(self):
        return self.builder.get_object("warn_check")

    def destroy(self):
        self.window.destroy()

    def on_close(self, *_):
        if self._do_continue:
            settings.show_fast_flag_warning = self.warn_check.get_active()
            settings.save()

        self._callback(self._do_continue)

    def abort(self, *_):
        self._do_continue = False
        self.destroy()

    def open_editor(self, *_):
        self._do_continue = True
        self.destroy()

    def show_forum_post(self, link_button):
        pass

    def show(self):
        self.window.show()
