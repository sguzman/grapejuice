import json
from typing import List


class FastFlag:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def is_a(self, cls):
        return isinstance(self.value, cls)

    def __lt__(self, other):
        if isinstance(other, FastFlag):
            return self.name < other.name

        return -1

    def __repr__(self):
        return "FFlag '{}': {}".format(self.name, self.value)


class FastFlagList:
    def __init__(self):
        self._list: List[FastFlag] = list()

    def clear(self):
        self._list = list()

    def import_file(self, fast_flags_path):
        with open(fast_flags_path, "r") as fp:
            json_object = json.load(fp)
            self._list = list(map(lambda t: FastFlag(*t), json_object.items()))
            self._list.sort()

    def __iter__(self):
        for flag in self._list:
            yield flag
