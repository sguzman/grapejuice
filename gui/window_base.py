from gi.repository import Gtk


class WindowBase:
    def __init__(self, glade_path, handler_class=None):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_path)
        if handler_class:
            self.builder.connect_signals(handler_class())
