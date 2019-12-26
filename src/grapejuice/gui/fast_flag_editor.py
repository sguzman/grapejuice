import os
from typing import Union, Tuple

from gi.repository import Gtk

from grapejuice_common import robloxctrl
from grapejuice_common import variables
from grapejuice_common.fast_flags import FastFlagList, FastFlag
from grapejuice_common.gtk_stuff import WindowBase


def flag_to_widget(flag: FastFlag) -> Union[None, Tuple]:
    widget = None

    if flag.is_a(bool):
        widget = Gtk.Switch()
        widget.set_active(flag.value)

        get_value = lambda: widget.get_active()

    elif flag.is_a(str):
        widget = Gtk.Entry()
        widget.set_text(flag.value)
        widget.set_hexpand(True)
        widget.set_hexpand_set(True)

        get_value = lambda: widget.get_text()

    elif flag.is_a(int):
        adjustment = Gtk.Adjustment()
        adjustment.set_step_increment(1.0)
        adjustment.set_upper(2147483647)
        adjustment.set_value(flag.value)

        widget = Gtk.SpinButton()
        widget.set_adjustment(adjustment)
        widget.set_value(flag.value)

        get_value = lambda: int(adjustment.get_value())

    else:
        return None

    return widget, get_value


class FastFlagEditor(WindowBase):
    def __init__(self):
        super().__init__(variables.fast_flag_editor_glade(), self)

        self._fast_flags = FastFlagList().import_file(variables.wine_roblox_studio_app_settings())

        client_settings_path = robloxctrl.locate_client_settings()
        if client_settings_path is not None and os.path.exists(client_settings_path):
            self._fast_flags.overlay_flags(FastFlagList().import_file(client_settings_path))

        self._flag_refs = dict()

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
        def on_change(v):
            print("Change", flag.name, flag.value)
            flag.value = v

        builder = self._create_builder()

        wnd = builder.get_object("_row_template_container")
        row = builder.get_object("fast_flag_row")
        wnd.remove(row)

        name_label = builder.get_object("fflag_name_label")
        name_label.set_text(flag.name)

        widgets = builder.get_object("fast_flag_widgets")

        widget, get_value = flag_to_widget(flag)
        self._flag_refs[flag] = get_value

        if widget is not None:
            widgets.add(widget)
            widget.show()

        return row

    def _input_values_to_flags(self):
        for flag, v in self._flag_refs.items():
            flag.value = v()

    def save_flags_to_studio(self, *_):
        self._input_values_to_flags()
        changed_flags = self._fast_flags.get_changed_flags()
        save_path = robloxctrl.locate_client_settings()

        changed_flags.export_to_file(save_path)
