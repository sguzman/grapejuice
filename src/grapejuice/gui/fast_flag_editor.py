import os
from typing import Union

from gi.repository import Gtk

from grapejuice_common import robloxctrl
from grapejuice_common import variables
from grapejuice_common.fast_flags import FastFlagList, FastFlag
from grapejuice_common.gtk.GtkPaginator import GtkPaginator
from grapejuice_common.gtk.gtk_stuff import WindowBase
from grapejuice_common.paginator import Paginator


class WidgetStuff:
    def __init__(self, widget, get_value, set_value):
        self.widget = widget
        self.get_value = get_value
        self.set_value = set_value
        self.icon_changes: Union[None, Gtk.Image] = None
        self.reset_button: Union[None, Gtk.Button] = None


def flag_to_widget(flag: FastFlag, on_changed: callable = None) -> Union[None, WidgetStuff]:
    widget = None

    if flag.is_a(bool):
        widget = Gtk.Switch()
        widget.set_active(flag.value)
        widget.set_vexpand(False)
        widget.set_vexpand_set(True)

        def get_value():
            return widget.get_active()

        def set_value(v):
            widget.set_active(v)

        if on_changed is not None:
            widget.connect("state-set", on_changed)

    elif flag.is_a(str):
        widget = Gtk.Entry()
        widget.set_text(flag.value)
        widget.set_hexpand(True)
        widget.set_hexpand_set(True)

        def get_value():
            return widget.get_text()

        def set_value(v):
            widget.set_text(str(v))

        if on_changed is not None:
            widget.connect("changed", on_changed)

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

        if on_changed is not None:
            adjustment.connect("value-changed", on_changed)

    else:
        return None

    return WidgetStuff(widget, get_value, set_value)


class FastFlagEditor(WindowBase):
    def __init__(self):
        super().__init__(variables.fast_flag_editor_glade(), self)

        self._fast_flags = FastFlagList().import_file(variables.wine_roblox_studio_app_settings())

        client_settings_path = robloxctrl.locate_client_app_settings()
        if client_settings_path is not None and os.path.exists(client_settings_path):
            self._fast_flags.overlay_flags(FastFlagList().import_file(client_settings_path))

        self._paginator = Paginator(self._fast_flags, 50)
        self._gtk_paginator = GtkPaginator(self._paginator)
        self.gtk_pager_box.add(self._gtk_paginator.get_root_widget())

        self._flag_refs = dict()
        self._rows = dict()
        self._displayed_rows = list()

        self._populate()
        self._paginator.paged.add_listener(self._populate)

        self.__unsaved_changes = False

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

        self._update_change_icons()

    @property
    def _unsaved_changes(self):
        return self.__unsaved_changes

    @_unsaved_changes.setter
    def _unsaved_changes(self, v):
        self.__unsaved_changes = v

        if self.__unsaved_changes:
            self.gtk_header.set_subtitle("Unsaved changes!")

        else:
            self.gtk_header.set_subtitle("")

    @property
    def window(self):
        return self.builder.get_object("fast_flag_editor")

    @property
    def gtk_fast_flag_list(self):
        return self.builder.get_object("fast_flag_list")

    @property
    def gtk_pager_box(self):
        return self.builder.get_object("paginator_box")

    @property
    def gtk_header(self):
        return self.builder.get_object("fast_flag_editor_header")

    @property
    def fast_flag_scroll(self):
        return self.builder.get_object("fast_flag_scroll")

    def new_row(self, flag: FastFlag):
        builder = self._create_builder()

        row = builder.get_object("fast_flag_row")

        name_label = builder.get_object("fflag_name_label")
        name_label.set_text(flag.name)

        widgets = builder.get_object("fast_flag_widgets")
        icon_changes = builder.get_object("icon_flag_changes")
        reset_button = builder.get_object("fflag_reset_button")

        stuff = None

        def reset_flag(*_):
            flag.reset()
            stuff.set_value(flag.value)
            reset_button.hide()

        reset_button.connect("clicked", reset_flag)

        def on_widget_changed(*_):
            flag.value = stuff.get_value()
            self._update_change_icons()

            if flag.has_changed and not flag.is_a(bool):
                reset_button.show()

            else:
                reset_button.hide()

            self._unsaved_changes = True

        stuff = flag_to_widget(flag, on_widget_changed)
        stuff.icon_changes = icon_changes
        stuff.reset_button = reset_button

        if stuff and stuff.widget is not None:
            self._flag_refs[flag] = stuff
            widgets.add(stuff.widget)

        wrapper = Gtk.ListBoxRow()
        wrapper.add(row)

        return wrapper

    def _input_values_to_flags(self):
        for flag, ref in self._flag_refs.items():
            flag.value = ref.get_value()

    def _flags_to_inputs(self):
        self._fast_flags.sort()

        for flag in filter(lambda f: f in self._flag_refs, self._fast_flags):
            ref = self._flag_refs[flag]
            ref.set_value(flag.value)

        self._paginator.paged()

    def _update_change_icons(self):
        for flag, ref in self._flag_refs.items():
            if flag.has_changed:
                ref.icon_changes.show()
                if not flag.is_a(bool):
                    ref.reset_button.show()

            else:
                ref.icon_changes.hide()
                ref.reset_button.hide()

            if flag.is_a(bool):
                ref.reset_button.hide()

    def save_flags_to_studio(self, *_):
        self._input_values_to_flags()
        changed_flags = self._fast_flags.get_changed_flags()
        save_path = robloxctrl.locate_client_app_settings()

        changed_flags.export_to_file(save_path)

        self._unsaved_changes = False

    def on_search_changed(self, search_entry):
        query = search_entry.get_text().lower()

        if query:
            def filter_function(flags_list):
                return filter(lambda flag: query in flag.name.lower(), flags_list)

            self._paginator.filter_function = filter_function

        else:
            self._paginator.filter_function = None

    def reset_all_flags(self, *_):
        self._fast_flags.reset_all_flags()
        self._flags_to_inputs()
        self._unsaved_changes = False

    def delete_user_flags(self, *_):
        self.reset_all_flags()

        path = robloxctrl.locate_client_app_settings()
        if os.path.exists(path):
            os.remove(path)
