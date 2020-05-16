import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
project_path = here
src_path = os.path.join(project_path, "src")
readme_path = os.path.join(project_path, "README.md")
requirements_path = os.path.join(project_path, "requirements.txt")

sys.path.insert(0, src_path)

from setuptools import setup, find_packages

import grapejuice.__about__ as __about__

with open(readme_path, "r") as fp:
    long_description = fp.read()

setup(
    name="grapejuice",
    author=__about__.author_name,
    author_email=__about__.author_email,
    version=__about__.package_version,
    description=__about__.package_description,
    license=__about__.package_license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__about__.package_repository,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Programming Language :: Python :: 3.7'
    ],
    keywords=["grapejuice wine roblox studio"],
    packages=find_packages("src", exclude=[
        "grapejuice_packaging",
        "grapejuice_packaging.*",
        "tests",
        "tests.*"
    ]),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "psutil",
        "pip",
        "PyGObject",
        "PyGObject-stubs",
        "packaging",
        "wheel",
        "setuptools",
        "dbus-python",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "grapejuice=grapejuice.__main__:main",
            "grapejuiced=grapejuiced.__main__:main"
        ]
    }
)
