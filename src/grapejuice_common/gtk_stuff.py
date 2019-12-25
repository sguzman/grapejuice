import sys


def gtk_boot(main_function, *args, **kwargs):
    assert callable(main_function)
    sys.argv[0] = "Grapejuice"

    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    main_function(*args, **kwargs)

    Gtk.main()


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
