import glob
import os
import shutil
import subprocess
from abc import ABC


def setup_py_is_here():
    assert os.path.exists("setup.py"), "Could not find setup.py"


class Platform(ABC):
    @staticmethod
    def path_build():
        return os.path.abspath("build")

    @staticmethod
    def path_dist():
        return os.path.abspath("dist")

    @staticmethod
    def clean():
        setup_py_is_here()

        if os.path.exists(Platform.path_build()):
            shutil.rmtree(Platform.path_build())

        if os.path.exists(Platform.path_dist()):
            shutil.rmtree(Platform.path_dist())

    @staticmethod
    def build_wheel():
        subprocess.check_call(["python3", "setup.py", "bdist_wheel"])

    @staticmethod
    def list_wheels():
        return glob.glob(os.path.join(Platform.path_dist(), "*.whl"))

    def before_package(self):
        self.build_wheel()

    def package(self):
        pass

    def after_package(self):
        pass

    def run(self) -> int:
        self.clean()
        self.before_package()
        self.package()
        self.after_package()

        return 0

    def __call__(self, *args, **kwargs):
        return self.run()
