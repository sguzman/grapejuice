from grapejuice_common import WindowBase
from grapejuice_common import variables
from grapejuice_registry.snapshot import Snapshot
from sparklepop.gui.snapshot_view_model import SnapshotViewModel


class SnapshotWidget:
    def __init__(self, parent, snap: Snapshot):
        from gi.repository import Gtk

        self.parent = parent
        self.snap = snap
        self.container = Gtk.Button(always_show_image=False)
        self.container.set_focus_on_click(False)

        self.box = Gtk.Box()
        self.box.set_orientation(1)
        sides = ("top", "left", "bottom", "right")
        for side in sides:
            getattr(self.box, "set_margin_" + side)(10)

        self.container.add(self.box)

        self.name_label = Gtk.Label(label=snap.name)
        self.name_label.set_xalign(0)
        self.box.add(self.name_label)

        self.datetime_label = Gtk.Label(label=snap.datetime)
        self.datetime_label.set_xalign(0)
        self.datetime_label.set_margin_bottom(5)
        self.box.add(self.datetime_label)

        self.description_label = Gtk.Label(label=snap.description)
        self.description_label.set_xalign(0)
        self.description_label.set_line_wrap(True)
        self.box.add(self.description_label)

        self.bad_indicator = Gtk.Image()
        self.bad_indicator.set_halign(Gtk.Align.END)
        self.bad_indicator.set_margin_top(5)
        self.displayed_broken = snap.broken
        self.box.add(self.bad_indicator)

        self.container.connect("clicked", self._on_click)

    def _on_click(self, *args):
        self.parent.select_snapshot(self)

    @property
    def displayed_name(self):
        return self.name_label.get_text()

    @displayed_name.setter
    def displayed_name(self, value):
        self.name_label.set_text(value)

    @property
    def displayed_broken(self):
        return self.snap.broken

    @displayed_broken.setter
    def displayed_broken(self, value):
        from gi.repository import Gtk
        icon = "gtk-dialog-error" if value else "gtk-yes"
        self.bad_indicator.set_from_stock(icon, Gtk.IconSize.BUTTON)

    @property
    def displayed_description(self):
        return self.description_label.get_text()

    @displayed_description.setter
    def displayed_description(self, value):
        self.description_label.set_text(value)


class MainWindow(WindowBase):
    snapshot_model = None
    selected_snap_widget: SnapshotWidget = None
    setting_snap_widget = False
    made_changes = False

    def __init__(self):
        from sparklepop.gui import SparklepopHandlers

        def create_handlers():
            handlers = SparklepopHandlers()
            handlers.parent = self
            return handlers

        super().__init__(variables.sparklepop_glade(), create_handlers)
        self._build()
        self.hide_info_panel()

    def _snapshot_box(self):
        return self.builder.get_object("snapshot_box")

    def _snapshot_info_panel(self):
        return self.builder.get_object("snapshot_info_panel")

    def _snapshot_info_id(self):
        return self.builder.get_object("snapshot_info_id")

    def _snapshot_info_name(self):
        return self.builder.get_object("snapshot_info_name")

    def _snapshot_info_broken(self):
        return self.builder.get_object("snapshot_info_broken")

    def _snapshot_info_description(self):
        return self.builder.get_object("snapshot_info_description")

    def _window(self):
        return self.builder.get_object("sparklepop_main")

    def hide_info_panel(self):
        self._snapshot_info_panel().hide()

    def show_info_panel(self):
        self._snapshot_info_panel().show()

    def show(self):
        self.populate_snapshots()
        self._window().show()

    def populate_snapshots(self):
        from gi.repository import Gtk
        snapshot_box = self._snapshot_box()

        for child in snapshot_box.get_children():
            snapshot_box.remove(child)

        first_pfx = True
        self.snapshot_model = SnapshotViewModel()
        for pfx in self.snapshot_model:
            pfx_label = Gtk.Label(use_markup=True)
            pfx_label.set_markup("<span size='large' weight='bold'>Prefix {}</span>".format(pfx.id))
            pfx_label.set_xalign(0)
            pfx_label.set_selectable(False)
            pfx_label.set_margin_top(0 if first_pfx else 20)
            snapshot_box.add(pfx_label)

            pfx_container = Gtk.FlowBox(homogeneous=True)

            for snap in pfx:
                widget = SnapshotWidget(self, snap)
                pfx_container.add(widget.container)

            first_pfx = False
            snapshot_box.add(pfx_container)

        snapshot_box.show_all()

    def select_snapshot(self, widget: SnapshotWidget):
        self.setting_snap_widget = True

        from gi.repository import Gtk
        if self.selected_snap_widget is not None:
            self.save_snap()

        self.selected_snap_widget = widget
        if widget is not None:
            snap = widget.snap
            self._snapshot_info_id().set_text(snap.id)
            self._snapshot_info_name().set_text(snap.name)
            self._snapshot_info_broken().set_active(snap.broken)

            buf = Gtk.TextBuffer()
            buf.set_text(snap.description)
            self._snapshot_info_description().set_buffer(buf)
            self.show_info_panel()

        self.made_changes = False
        self.setting_snap_widget = False

    def _info_name(self):
        return self._snapshot_info_name().get_text()

    def _info_broken(self):
        return self._snapshot_info_broken().get_active()

    def _info_description(self):
        buf = self._snapshot_info_description().get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

    def on_snapshot_changed(self):
        if self.setting_snap_widget or self.selected_snap_widget is None:
            return

        self.selected_snap_widget.displayed_name = self._info_name()
        self.selected_snap_widget.displayed_broken = self._info_broken()
        self.selected_snap_widget.displayed_description = self._info_description()

        self.made_changes = True

    def save_snap(self):
        if self.selected_snap_widget is None or not self.made_changes:
            return

        snap = self.selected_snap_widget.snap
        snap.name = self._info_name()
        snap.broken = self._info_broken()
        snap.description = self._info_description()
        snap.update()
