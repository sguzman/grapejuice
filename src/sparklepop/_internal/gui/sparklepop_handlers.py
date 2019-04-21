from gi.repository import Gtk


class SparklepopHandlers:
    def on_destroy(self, *args):
        Gtk.main_quit()
