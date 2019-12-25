class WindowBase:
    def __init__(self, glade_path, handlers=None):
        self._glade_path = glade_path
        self._handlers = handlers

        self._build()

    def _build(self):
        from gi.repository import Gtk

        self.builder = Gtk.Builder()
        self.builder.add_from_file(self._glade_path)

        if self._handlers:
            self.builder.connect_signals(self._handlers)
