# -*- coding: utf-8 -*-
# type: ignore
from setuptools import find_namespace_packages
from setuptools import setup

from src.facedetectionapp import __author__
from src.facedetectionapp import __author_email__
from src.facedetectionapp import __description__
from src.facedetectionapp import __license__
from src.facedetectionapp import __long_description__
from src.facedetectionapp import __name__
from src.facedetectionapp import __url__
from src.facedetectionapp import __version__

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


with open("requirements-dev.txt") as f:
    test_requirements = f.read().splitlines()


setup(
    name=__name__,
    author=__author__,
    author_email=__author_email__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description=__description__,
    install_requires=requirements,
    include_package_data=True,
    license=__license__,
    long_description_content_type="text/markdown",
    long_description=__long_description__,
    packages=find_namespace_packages("src", exclude=["docs", "tests"]),
    package_dir={"": "src"},
    tests_require=test_requirements,
    url=__url__,
    version=__version__,
    python_requires=">=3.10",
)
