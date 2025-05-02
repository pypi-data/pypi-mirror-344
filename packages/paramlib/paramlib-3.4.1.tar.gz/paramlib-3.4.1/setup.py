#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**
Run this program to make of the entire module, repository, installable.

Created: {CREATION_DATE}
Current Version: 3.4.1
"""

#----------------#
# Import modules #
#----------------#

from setuptools import setup, find_packages
from datetime import datetime as dt

#-------------------#
# Define parameters #
#-------------------#

TIME_FMT_STR = "%Y-%m-%d %H:%M:%S"
CREATION_DATE = dt.now().strftime(TIME_FMT_STR)
PACKAGE_NAME = "paramlib"

#--------------------------------#
# Define the metadata dictionary #
#--------------------------------#

METADATA_DICT = dict(
    name=PACKAGE_NAME,
    version="3.4.1",
    description="A Python library for managing configuration parameters and constants, centralizing access to application-wide settings and global constants",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jon Ander Gabantxo",
    author_email="jagabantxo@gmail.com",
    url="https://github.com/EusDancerDev/paramlib",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    license="MIT",
    keywords="parameters, configuration, constants, python",
    project_urls={
        "Bug Reports": "https://github.com/EusDancerDev/paramlib/issues",
        "Source": "https://github.com/EusDancerDev/paramlib",
        "Documentation": "https://github.com/EusDancerDev/paramlib#readme",
    },
)

# Pass it to the 'setup' module #
setup(**METADATA_DICT)
