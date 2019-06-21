class WindowBase:
    def __init__(self, glade_path, handler_class=None):
        self._glade_path = glade_path
        self._handler_class = handler_class

    def _build(self):
        from gi.repository import Gtk

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self._glade_path)
        if self._handler_class:
            self.builder.connect_signals(self._handler_class())
