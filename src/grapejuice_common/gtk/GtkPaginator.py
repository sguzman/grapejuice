from grapejuice_common.gtk.grapejuice_component import GrapejuiceComponent
from grapejuice_common.paginator import Paginator


class GtkPaginator(GrapejuiceComponent):
    def __init__(self, paginator: Paginator):
        super().__init__()
        self._paginator = paginator

        def go_back(*_):
            self._paginator.previous()

        def go_forward(*_):
            self._paginator.next()

        def update_display():
            self._label.set_text(self._label_text)

        self._button_previous.connect("clicked", go_back)
        self._button_next.connect("clicked", go_forward)
        self._paginator.paged.add_listener(update_display)

        update_display()

    @property
    def _label(self):
        return self._builder.get_object("paginator_label")

    @property
    def _label_text(self):
        return "{}/{}".format(self._paginator.current_page_index + 1, self._paginator.n_pages)

    @property
    def _button_previous(self):
        return self._builder.get_object("paginator_previous")

    @property
    def _button_next(self):
        return self._builder.get_object("paginator_next")

    def get_root_widget(self):
        return self._builder.get_object("paginator")
