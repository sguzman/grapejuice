from grapejuice_common.updates.update_provider import UpdateProvider, UpdateError


class SystemUpdateProvider(UpdateProvider):
    @staticmethod
    def can_update() -> bool:
        return False

    def do_update(self):
        raise UpdateError("Grapejuice cannot upgrade a system package")
