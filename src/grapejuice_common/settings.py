import atexit
import json
import os
import time

from grapejuice_common import variables


class UserSettings:
    def __init__(self, file_location=variables.grapejuice_user_settings()):
        self._location = file_location

        self.performed_post_install = False
        self.n_player_dialogs_remain = 3
        self.show_fast_flag_warning = True

        self._update_last_run()

        self.load()

    def _filtered_dict(self):
        d = dict()

        for k, v in self.__dict__.items():
            if not k.startswith("_"):
                d[k] = v

        return d

    def _update_last_run(self):
        self.last_run = int(time.time() // 1)

    def _accept_json(self, o):
        self_dict = self.__dict__

        for k, v in o.items():
            self_dict[k] = v

    def load(self):
        if os.path.exists(self._location):
            with open(self._location, "r") as fp:
                json_object = json.load(fp)
                self._accept_json(json_object)

        else:
            self.save()

    def save(self):
        self._update_last_run()
        with open(self._location, "w+") as fp:
            json.dump(self._filtered_dict(), fp)


settings = UserSettings()


def save_settings():
    print("Saving settings...")
    settings.save()


atexit.register(save_settings)
