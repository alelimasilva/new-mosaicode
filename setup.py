#!/usr/bin/env python3
"""
Setup script for Mosaicode
"""

from setuptools import setup, find_packages

setup(
    name="mosaicode",
    version="1.0.4.dev1",
    description="Automatic Programming Tool",
    author="ALICE: Arts Lab in Interfaces, Computers, and Else",
    author_email="mosaicode-dev@googlegroups.com",
    license="GNU GPL3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pycairo>=1.20.0",
        "PyGObject>=3.40.0",
        "pgi",
    ],
    python_requires=">=3.9",
    scripts=[
        'launcher/mosaicode',
        'scripts/mosaicode.sh',
        'scripts/mosaicode.1',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: GNU/Linux",
        "Programming Language :: Python 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Digital Art :: VPL",
    ],
) 