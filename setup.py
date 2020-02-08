import os
import sys

here = os.path.abspath(os.path.dirname(__file__))
project_path = here
src_path = os.path.join(project_path, "src")
readme_path = os.path.join(project_path, "README.md")
requirements_path = os.path.join(project_path, "requirements.txt")

sys.path.insert(0, src_path)

from setuptools import setup, find_packages

import grapejuice_packaging.metadata as metadata

with open(readme_path, "r") as fp:
    long_description = fp.read()

with open(requirements_path, "r") as fp:
    requirements = [r.lstrip().rstrip() for r in fp.readlines()]

setup(
    name="grapejuice",
    author=metadata.author_name,
    author_email=metadata.author_email,
    version=metadata.package_version,
    description=metadata.package_description,
    license=metadata.package_license,
    platform=metadata.package_platform,
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
    }
)
