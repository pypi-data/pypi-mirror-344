#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Note**
Run this program to make of the entire module, repository, installable.

Created: {CREATION_DATE}
Current Version: 3.2.2
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
PACKAGE_NAME = "geosptools"
CREATION_DATE = dt.now().strftime(TIME_FMT_STR)

#--------------------------------#
# Define the metadata dictionary #
#--------------------------------#

METADATA_DICT = dict(
    name=PACKAGE_NAME,
    version="3.2.2",
    description="A geospatial data processing and analysis toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jon Ander Gabantxo",
    author_email="jagabantxo@gmail.com",
    url="https://github.com/EusDancerDev/geosptools",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "filewise>=3.7.0",
        "pygenutils>=15.10.0",
        "paramlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",	
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    keywords="geospatial, GIS, spatial analysis, remote sensing",
    project_urls={
        "Bug Reports": "https://github.com/EusDancerDev/geosptools/issues",
        "Source": "https://github.com/EusDancerDev/geosptools",
        "Documentation": "https://github.com/EusDancerDev/geosptools#readme",
    },
)

# Pass it to the 'setup' module #
setup(**METADATA_DICT)
