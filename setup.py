import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
project_path = here
src_path = os.path.join(project_path, "src")
readme_path = os.path.join(project_path, "README.md")
requirements_path = os.path.join(project_path, "requirements.txt")

sys.path.insert(0, src_path)

from setuptools import setup, find_packages, Command

import grapejuice_packaging.metadata as metadata

with open(readme_path, "r") as fp:
    long_description = fp.read()

with open(requirements_path, "r") as fp:
    requirements = [r.lstrip().rstrip() for r in fp.readlines()]


class PackageDebian(Command):
    description = "Package Grapejuice for debian"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from grapejuice_packaging.__main__ import main as packaging_main
        packaging_main([sys.argv[0], "debian"])


setup(
    name="grapejuice",
    author=metadata.author_name,
    author_email=metadata.author_email,
    version=metadata.package_version,
    description=metadata.package_description,
    license=metadata.package_license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=metadata.package_repository,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Programming Language :: Python :: 3.7'
    ],
    keywords=["grapejuice wine roblox studio"],
    packages=find_packages("src", exclude=("grapejuice_packaging",)),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "grapejuice=grapejuice.__main__:main",
            "grapejuiced=grapejuiced.__main__:main"
        ]
    },
    cmdclass={
        "package_debian": PackageDebian
    }
)
