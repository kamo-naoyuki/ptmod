#!/usr/bin/env python3
import os
from setuptools import find_packages
from setuptools import setup


dirname = os.path.dirname(__file__)
setup(
    name="ptmod",
    version="0.0.0",
    url="http://github.com/kamo-naoyuki/ptmod",
    author="Naoyuki Kamo",
    description="A Command line utility to modify serialized PyTorch model states.",
    long_description=open(os.path.join(dirname, "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["ptmod"],
    entry_points={
        "console_scripts": [
            "ptmod = ptmod:ptmod_main",
            "ptmod-ls = ptmod:ptmod_ls",
            "ptmod-rm = ptmod:ptmod_rm",
            "ptmod-cp = ptmod:ptmod_cp",
            "ptmod-average = ptmod:ptmod_average",
            "ptmod-sum = ptmod:ptmod_sum",
        ],
    },
    license="MIT",
    python_requires=">=3.6.0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
