#!/usr/bin/env python

import os
import sys
from shutil import rmtree

from setuptools import Command, setup

VERSION = "0.1.0"


class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(msg):
        print(f"\033[1m{msg}\033[0m")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(ROOT, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system(f"{sys.executable} setup.py sdist bdist_wheel --universal")

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system(f"git tag v{VERSION}")
        os.system("git push --tags")

        exit()


ROOT = os.path.dirname(__file__)

try:
    with open(os.path.join(ROOT, "README.md")) as fp:
        long_description = "\n" + fp.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="Rando",
    version=VERSION,
    description="rando is a weighted random generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brandon LeBlanc",
    author_email="brandon@leblanc.codes",
    url="https://github.com/demosdemon/rando",
    py_modules=["rando"],
    include_package_data=False,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    cmdclass={"upload": UploadCommand},
)
