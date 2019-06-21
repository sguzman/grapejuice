from gi.repository import Gtk


class SparklepopHandlers:
    parent = None
    flag = True

    def on_destroy(self, *args):
        Gtk.main_quit()

    def sig_debug(self, *args):
        if self.flag:
            self.parent.hide_info_panel()
        else:
            self.parent.show_info_panel()

        self.flag = not self.flag

    def snapshot_info_changed(self, *args):
        self.parent.on_snapshot_changed()

    def snapshot_info_changed(self, *args):
        self.parent.on_snapshot_changed()

    def create_snapshot(self, *args):
        import grapejuice_registry.snapshot as snapshot
        snapshot.create_snapshot()
        self.parent.populate_snapshots()
