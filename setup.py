#!/usr/bin/env python
#
# Copyright (C) 2009-2026 James Cherti
# URL: https://github.com/jamescherti/ansible-cleanup
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
#
"""A setuptools based setup module to install ansible-cleanup."""


from pathlib import Path

from setuptools import find_packages, setup

PROJECT_ROOT: Path = Path(__file__).parent.resolve()
README_PATH: Path = PROJECT_ROOT / "README.md"

# Define your project dependencies here
DEPENDENCIES: list[str] = [
    "ansible-core>=2.14.0",
]

setup(
    name="ansible-cleanup",
    version="0.9.9",
    description=("Utilities for detecting unused imports and variables "
                 "in Ansible projects"),
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="James Cherti",
    url="https://github.com/jamescherti/ansible-cleanup",
    python_requires=">=3.10",
    install_requires=DEPENDENCIES,
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
        ],
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Utilities",
    ],
    keywords=[
        "ansible",
        "lint",
        "cleanup",
        "static-analysis",
    ],
    entry_points={
        "console_scripts": [
            (
                "ansible-cleanup-imports="
                "ansible_cleanup.cli_find_unused_tasks:"
                "command_line_interface"
            ),
            (
                "ansible-cleanup-vars="
                "ansible_cleanup.cli_find_unused_vars:"
                "command_line_interface"
            ),
        ],
    },
)
