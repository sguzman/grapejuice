import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
project_path = here
src_path = os.path.join(project_path, "src")
readme_path = os.path.join(project_path, "README.md")
requirements_path = os.path.join(project_path, "requirements.txt")

sys.path.insert(0, src_path)

from setuptools import setup, find_packages

from grapejuice.__init__ import __version__ as grapejuice_version

with open(readme_path, "r") as fp:
    long_description = fp.read()

with open(requirements_path, "r") as fp:
    requirements = [r.lstrip().rstrip() for r in fp.readlines()]

setup(
    name="grapejuice",
    version=grapejuice_version,
    description="A simple wine+roblox management application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/brinkervii/grapejuice",
    classifiers=[
        "Development Status :: 4 - Beta",
        'Programming Language :: Python :: 3.7'
    ],
    keywords=["grapejuice wine roblox studio"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "grapejuice=grapejuice.__main__:main",
            "grapejuiced=grapejuiced.__main__:main"
        ]
    }
)
