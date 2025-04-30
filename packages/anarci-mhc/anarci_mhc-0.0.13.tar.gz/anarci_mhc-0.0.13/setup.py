import os
import shutil
import sys
from setuptools import setup, find_packages

setup(
    name="anarci-mhc",
    version="0.0.13",
    description="Antibody Numbering and Receptor ClassIfication",
    author="Dunbar & Quast",
    author_email="opig@stats.ox.ac.uk",
    url="http://opig.stats.ox.ac.uk/webapps/ANARCI",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "anarci": [
            "dat/HMMs/*",
            "germlines.py",
            "mhc_alleles.py",
        ],
    },
    data_files=[("bin", ["bin/muscle", "bin/muscle_macOS", "bin/ANARCI"])],
    install_requires=["biopython", "pyhmmer"],
    scripts=["bin/ANARCI"],
)
