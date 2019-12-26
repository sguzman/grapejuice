import json
import os
from typing import List, Iterable


class FastFlag:
    def __init__(self, name, value):
        self._name = name
        self._original_value = value
        self.value = value

    def is_a(self, cls):
        return isinstance(self.value, cls)

    @property
    def name(self):
        return self._name

    @property
    def has_changed(self):
        return self.value != self._original_value

    def to_tuple(self):
        return self.name, self.value

    def __lt__(self, other):
        if isinstance(other, FastFlag):
            return self._name < other.name

        return -1

    def __repr__(self):
        return "FFlag '{}': {}".format(self._name, self.value)


class FastFlagList:
    def __init__(self, initial_values: Iterable[FastFlag] = None):
        if initial_values is None:
            self._list: List[FastFlag] = list()

        else:
            self._list = list(initial_values)

    def clear(self):
        self._list = list()

    def import_file(self, fast_flags_path):
        with open(fast_flags_path, "r") as fp:
            json_object = json.load(fp)
            self._list = list(map(lambda t: FastFlag(*t), json_object.items()))
            self._list.sort()

    def export_to_file(self, fast_flags_path):
        os.makedirs(os.path.dirname(fast_flags_path), exist_ok=True)

        with open(fast_flags_path, "w+") as fp:
            json.dump(self.to_dict(), fp)

    def get_changed_flags(self):
        return FastFlagList(initial_values=filter(lambda flag: flag.has_changed, self._list))

    def to_dict(self):
        return dict(map(lambda flag: flag.to_tuple(), self))

    def __iter__(self):
        for flag in self._list:
            yield flag
