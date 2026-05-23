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
"""A setuptools based setup module."""

from setuptools import find_packages, setup

setup(
    name="ansible-cleanup",
    version="0.9.9",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ansible-cleanup-unused-imports=ansible_cleanup.cli_find_unused_tasks:"
            "command_line_interface",

            "ansible-cleanup-unused-vars=ansible_cleanup.cli_find_unused_vars:"
            "command_line_interface",
        ],
    },
)
