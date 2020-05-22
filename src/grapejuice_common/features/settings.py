import atexit
import json
import logging
import os
import time
from typing import Union

from grapejuice_common import variables

LOG = logging.getLogger(__name__)


class Setting:
    def __init__(self, key: str, display_name: str, default_value: Union[any, None] = None):
        self._key: str = key
        self._display_name: str = display_name
        self._default_value: Union[any, None] = default_value
        self._value: any = default_value

    def isinstance(self, v):
        return isinstance(self.value, v)

    def reset(self):
        self._value = self._default_value

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> Union[any, None]:
        return self._value

    @value.setter
    def value(self, v) -> None:
        if self._default_value is not None:
            assert type(self._default_value) is type(v)

        self._value = v

    @property
    def display_name(self) -> str:
        return self._display_name

    def __repr__(self) -> str:
        return f"'{self.key}' -> '{self.value}' ({self._default_value})"


class UserSettings:
    def __init__(self, file_location=variables.grapejuice_user_settings()):
        self._location = file_location

        self.performed_post_install = False
        self.n_player_dialogs_remain = 3
        self.show_fast_flag_warning = True

        self.wine_binary = Setting("wine_binary", "Wine binary", "")
        self.ignore_wine_version = Setting("ignore_wine_version", "Ignore Wine version", False)

        self._update_last_run()

        self.load()

    def _filtered_dict(self):
        d = dict()

        for k, v in self.__dict__.items():
            if isinstance(v, Setting):
                d[v.key] = v.value

            elif not k.startswith("_"):
                d[k] = v

        return d

    def _update_last_run(self):
        self.last_run = int(time.time() // 1)
        LOG.debug(f"Set last run time to {self.last_run}")

    def _accept_json(self, o):
        self_dict = self.__dict__

        LOG.debug("Loading JSON object into the settings file")

        for k, v in o.items():
            LOG.debug(f"Read '{k}' with value '{v}'")

            if k in self_dict:
                LOG.debug(f"Going to apply the value with key {k}")
                existing_value = self_dict[k]

                if isinstance(existing_value, Setting):
                    LOG.debug(f"Doing a special setting thing with {k}")
                    existing_value.value = v
                    continue

                else:
                    LOG.debug(f"Applying {k}")
                    self_dict[k] = v

            else:
                LOG.debug(f"Not going to apply a value with key {k}, because it is not on the settings object")

    def load(self):
        if os.path.exists(self._location):
            LOG.debug(f"Loading settings from '{self._location}'")

            with open(self._location, "r") as fp:
                json_object = json.load(fp)
                self._accept_json(json_object)

        else:
            LOG.debug("There is no settings file present, going to save one")
            self.save()

    def save(self):
        self._update_last_run()

        LOG.debug(f"Saving settings file to '{self._location}'")
        with open(self._location, "w+") as fp:
            json.dump(self._filtered_dict(), fp)

    def ui_facing_settings(self):
        return list(filter(lambda v: isinstance(v, Setting), self.__dict__.values()))


settings = UserSettings()


def save_settings():
    LOG.info("Saving settings...")
    settings.save()


atexit.register(save_settings)
