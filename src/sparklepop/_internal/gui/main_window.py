from grape_common import WindowBase
from grape_common import variables


class MainWindow(WindowBase):
    def __init__(self):
        from sparklepop._internal.gui.sparklepop_handlers import SparklepopHandlers
        super().__init__(variables.sparklepop_glade(), SparklepopHandlers)
        self._build()

    def _window(self):
        return self.builder.get_object("sparklepop_main")

    def show(self):
        self._window().show()
