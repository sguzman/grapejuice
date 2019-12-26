import math

from grapejuice_common.event import Event


class Paginator:
    def __init__(self, collection, page_size):
        self._collection = collection
        self._page_size = page_size
        self._current_page = 0

        self.paged = Event()

    @property
    def page(self):
        lower_limit = self._current_page * self._page_size
        upper_limit = min(len(self._collection), lower_limit + self._page_size)

        return self._collection[lower_limit:upper_limit]

    @property
    def current_page_index(self):
        return self._current_page

    @property
    def n_pages(self):
        return math.ceil(len(self._collection) / self._page_size)

    @property
    def at_last_page(self):
        return self._current_page >= self.n_pages - 1

    def next(self):
        self._current_page = min(self.n_pages - 1, self._current_page + 1)
        self.paged()

    def previous(self):
        self._current_page = max(0, self._current_page - 1)
        self.paged()
