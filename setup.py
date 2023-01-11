# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import find_namespace_packages
from setuptools import setup

VERSION = "0.0.1"

# parsing requirements generated from pip-compile
reqs_path = Path(__file__).parent / "requirements.txt"
install_requires = reqs_path.read_text().splitlines()

console_scripts = [
    "link_drugs = drug_analysis.main:link_drugs",
    "adhoc_processing = drug_analysis.main:adhoc_processing",
]



setup(
    name="drug_analysis",
    version=VERSION,
    description="Analysis pipeline for drug's mentions in articles and journals",
    url="https://github.com/alaameloh/drug_links_project",
    author="Alaa HOUIMEL",
    author_email="alaa.houimel@gmail.com",
    install_requires=install_requires,
    license="MIT",
    packages=find_namespace_packages(exclude=["data", "tests"]),
    entry_points={"console_scripts": console_scripts},
)
