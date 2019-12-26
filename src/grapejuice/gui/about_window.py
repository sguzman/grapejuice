from grapejuice import __version__ as grapejuice_version
from grapejuice_common import variables
from grapejuice_common.gtk.gtk_stuff import WindowBase


class AboutWindow(WindowBase):
    def __init__(self):
        super().__init__(variables.about_glade(), self)

        self.window.set_version(grapejuice_version)

    @property
    def window(self):
        return self.builder.get_object("grapejuice_about")

    def close_about(self, *_):
        self.window.destroy()

    def __del__(self):
        del self.builder
