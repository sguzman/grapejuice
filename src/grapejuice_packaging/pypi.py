import os
import subprocess

from grapejuice_packaging.packaging_platform import Platform


class PyPIPlatform(Platform):
    def after_package(self):
        subprocess.check_call(["twine", "upload", os.path.join(Platform.path_dist(), "*")])
