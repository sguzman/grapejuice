import grapejuice_common.variables as variables
from grapejuice_common import WindowBase, version


class AboutWindow(WindowBase):
    def __init__(self):
        super().__init__(variables.grapejuice_main_glade())
        self._build()

    def window(self):
        return self.builder.get_object("grapejuice_about")

    def run(self):
        w = self.window()
        w.set_version(str(version.local_version()))

        w.run()
        w.destroy()
