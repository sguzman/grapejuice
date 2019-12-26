from typing import Union

from gi.repository import Gtk

from grapejuice_common import variables
from grapejuice_common.fast_flags import FastFlagList, FastFlag
from grapejuice_common.gtk_stuff import WindowBase


def flag_to_widget(flag: FastFlag) -> Union[None, Gtk.Widget]:
    widget = None

    if flag.is_a(bool):
        widget = Gtk.Switch()
        widget.set_active(flag.value)

    elif flag.is_a(str):
        widget = Gtk.Entry()
        widget.set_text(flag.value)
        widget.set_hexpand(True)
        widget.set_hexpand_set(True)

    elif flag.is_a(int):
        adjustment = Gtk.Adjustment()
        adjustment.set_step_increment(1.0)
        adjustment.set_upper(2147483647)
        adjustment.set_value(flag.value)

        widget = Gtk.SpinButton()
        widget.set_adjustment(adjustment)
        widget.set_value(flag.value)

    return widget


class FastFlagEditor(WindowBase):
    def __init__(self):
        super().__init__(variables.fast_flag_editor_glade())

        self._fast_flags = FastFlagList()
        self._fast_flags.import_file(variables.wine_roblox_studio_app_settings())

        self._populate()

    def _populate(self):
        gtk_list = self.gtk_fast_flag_list

        for flag in self._fast_flags:
            row = self.new_row(flag)
            gtk_list.add(row)

    @property
    def window(self):
        return self.builder.get_object("fast_flag_editor")

    @property
    def gtk_fast_flag_list(self):
        return self.builder.get_object("fast_flag_list")

    def new_row(self, flag: FastFlag):
        builder = self._create_builder()

        wnd = builder.get_object("_row_template_container")
        row = builder.get_object("fast_flag_row")
        wnd.remove(row)

        name_label = builder.get_object("fflag_name_label")
        name_label.set_text(flag.name)

        widgets = builder.get_object("fast_flag_widgets")

        widget = flag_to_widget(flag)
        if widget is not None:
            widgets.add(widget)
            widget.show()

        return row
