import grapejuice._internal.update as update
import grapejuice._internal.variables as variables


def AboutWindow():
    from grapejuice._internal import WindowBase

    class AboutWindowC(WindowBase):
        def __init__(self):
            super().__init__(variables.grapejuice_main_glade())

        def window(self):
            return self.builder.get_object("grapejuice_about")

        def run(self):
            w = self.window()
            w.set_version(str(update.local_version()))

            w.run()
            w.destroy()

    return AboutWindowC()
