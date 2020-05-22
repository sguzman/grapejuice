import logging
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
project_path = here
src_path = os.path.join(project_path, "src")
readme_path = os.path.join(project_path, "README.md")

sys.path.insert(0, src_path)

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def read_file(path):
    with open(path, "r") as fp:
        return fp.read()


def main():
    import grapejuice.__about__ as __about__
    from grapejuice_packaging.local_install import InstallLocally

    setup(
        name="grapejuice",
        author=__about__.author_name,
        author_email=__about__.author_email,
        version=__about__.package_version,
        description=__about__.package_description,
        license=__about__.package_license,
        long_description=read_file(readme_path),
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
        },
        cmdclass={
            "install_locally": InstallLocally
        }
    )


if __name__ == '__main__':
    main()
