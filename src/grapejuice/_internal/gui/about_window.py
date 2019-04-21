import grape_common.variables as variables
import grapejuice._internal.update as update
from grape_common import WindowBase


class AboutWindow(WindowBase):
    def __init__(self):
        super().__init__(variables.grapejuice_main_glade())
        self._build()

    def window(self):
        return self.builder.get_object("grapejuice_about")

    def run(self):
        w = self.window()
        w.set_version(str(update.local_version()))

        w.run()
        w.destroy()
