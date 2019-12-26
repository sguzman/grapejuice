import sys


def gtk_boot(main_function, gtk_main=True, *args, **kwargs):
    assert callable(main_function)
    sys.argv[0] = "Grapejuice"

    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk

    main_function(*args, **kwargs)

    if gtk_main:
        Gtk.main()


def dialog(dialog_text):
    from gi.repository import Gtk

    gtk_dialog = Gtk.MessageDialog(
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=dialog_text
    )

    gtk_dialog.run()
    gtk_dialog.destroy()


class WindowBase:
    def __init__(self, glade_path, handlers=None):
        self._glade_path = glade_path
        self._handlers = handlers

        self._build()

    def _create_builder(self):
        from gi.repository import Gtk

        builder = Gtk.Builder()
        builder.add_from_file(self._glade_path)

        return builder

    def _build(self):
        self.builder = self._create_builder()

        if self._handlers:
            self.builder.connect_signals(self._handlers)
