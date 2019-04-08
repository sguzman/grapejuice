from setuptools import setup, find_packages

from grapejuice._internal.update import local_version

install_requires = []
with open("requirements.txt", "r") as file:
    for line in file.readlines():
        install_requires.append(line)

setup(
    name="grapejuice",
    version=str(local_version()),
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "tasks"]
    ),
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "grapejuice=grapejuice._internal:main"
        ]
    }
)
