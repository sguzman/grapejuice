from packaging import version

from grapejuice_common.updates.update_provider import UpdateProvider, UpdateError


class SystemUpdateProvider(UpdateProvider):
    def target_version(self) -> version.Version:
        return version.parse("0.0.0")

    def update_available(self) -> bool:
        return False

    def local_is_newer(self) -> bool:
        return False

    @staticmethod
    def can_update() -> bool:
        return False

    def do_update(self) -> None:
        raise UpdateError("Grapejuice cannot upgrade a system package")
