from abc import ABC, abstractmethod

from gi.repository import Gtk

from grapejuice_common import variables


class GrapejuiceComponent(ABC):
    def __init__(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(variables.grapejuice_components_glade())

    @abstractmethod
    def get_root_widget(self):
        pass
