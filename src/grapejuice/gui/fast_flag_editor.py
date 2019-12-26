import os
from typing import Union, Tuple

from gi.repository import Gtk

from grapejuice_common import robloxctrl
from grapejuice_common import variables
from grapejuice_common.fast_flags import FastFlagList, FastFlag
from grapejuice_common.gtk.GtkPaginator import GtkPaginator
from grapejuice_common.gtk.gtk_stuff import WindowBase
from grapejuice_common.paginator import Paginator


def flag_to_widget(flag: FastFlag) -> Union[None, Tuple]:
    widget = None

    if flag.is_a(bool):
        widget = Gtk.Switch()
        widget.set_active(flag.value)

        def get_value():
            return widget.get_active()

        def set_value(v):
            widget.set_active(v)

    elif flag.is_a(str):
        widget = Gtk.Entry()
        widget.set_text(flag.value)
        widget.set_hexpand(True)
        widget.set_hexpand_set(True)

        def get_value():
            return widget.get_text()

        def set_value(v):
            widget.set_text(str(v))

    elif flag.is_a(int):
        adjustment = Gtk.Adjustment()
        adjustment.set_step_increment(1.0)
        adjustment.set_upper(2147483647)
        adjustment.set_value(flag.value)

        widget = Gtk.SpinButton()
        widget.set_adjustment(adjustment)
        widget.set_value(flag.value)

        def get_value():
            return int(adjustment.get_value())

        def set_value(v):
            adjustment.set_value(int(v))

    else:
        return None

    return widget, get_value, set_value


class FastFlagEditor(WindowBase):
    def __init__(self):
        super().__init__(variables.fast_flag_editor_glade(), self)

        self._fast_flags = FastFlagList().import_file(variables.wine_roblox_studio_app_settings())

        client_settings_path = robloxctrl.locate_client_settings()
        if client_settings_path is not None and os.path.exists(client_settings_path):
            self._fast_flags.overlay_flags(FastFlagList().import_file(client_settings_path))

        self._paginator = Paginator(self._fast_flags, 50)
        self._gtk_paginator = GtkPaginator(self._paginator)
        self.gtk_pager_box().add(self._gtk_paginator.get_root_widget())

        self._flag_refs = dict()
        self._rows = dict()
        self._displayed_rows = list()

        self._populate()
        self._paginator.paged.add_listener(self._populate)

    def _populate(self):
        gtk_list = self.gtk_fast_flag_list

        for row in self._displayed_rows:
            gtk_list.remove(row)

        self._displayed_rows = list()

        for flag in self._paginator.page:
            if flag in self._rows:
                row = self._rows[flag]

            else:
                row = self.new_row(flag)
                self._rows[flag] = row

            gtk_list.add(row)
            self._displayed_rows.append(row)

        self.fast_flag_scroll.get_vadjustment().set_value(0)
        gtk_list.show_all()

    @property
    def window(self):
        return self.builder.get_object("fast_flag_editor")

    @property
    def gtk_fast_flag_list(self):
        return self.builder.get_object("fast_flag_list")

    def gtk_pager_box(self):
        return self.builder.get_object("paginator_box")

    @property
    def fast_flag_scroll(self):
        return self.builder.get_object("fast_flag_scroll")

    def new_row(self, flag: FastFlag):
        builder = self._create_builder()

        row = builder.get_object("fast_flag_row")

        name_label = builder.get_object("fflag_name_label")
        name_label.set_text(flag.name)

        widgets = builder.get_object("fast_flag_widgets")

        t = [*flag_to_widget(flag)]
        widget = t[0]

        if widget is not None:
            self._flag_refs[flag] = tuple(t[1:])
            widgets.add(widget)

        wrapper = Gtk.ListBoxRow()
        wrapper.add(row)

        return wrapper

    def _input_values_to_flags(self):
        for flag, v in self._flag_refs.items():
            flag.value = v[0]()

    def save_flags_to_studio(self, *_):
        self._input_values_to_flags()
        changed_flags = self._fast_flags.get_changed_flags()
        save_path = robloxctrl.locate_client_settings()

        changed_flags.export_to_file(save_path)
