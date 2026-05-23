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
"""Helpers."""

from __future__ import annotations

import configparser
import os
from collections.abc import Iterable
from pathlib import Path


class AnsibleConfig:
    def __init__(self, file_name: os.PathLike):
        """Parse 'ansible.cfg'."""
        self.file_name = file_name
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(file_name)

    def get(self, section: str, variable: str) -> str:
        return str(self.config_parser.get(section, variable))


def existing_file_with_ext(base_path: os.PathLike,
                           list_extensions: Iterable[str]) -> Path:
    """Return a path of an existing file that ends with one of the extensions
    provided.

    >>> one_of_ext_exists("file", [".yml", ".yaml"])
    'file.yaml'
    """
    base_path_str = str(base_path)

    for current_extension in list_extensions:
        new_path = Path(f"{base_path_str}{current_extension}")
        if new_path.exists():
            return new_path

    raise FileNotFoundError(
        f"File not found: {base_path_str} (Extensions: {list_extensions})"
    )


def find_yaml_files(path: os.PathLike) -> set[Path]:
    result = set()
    for file_name in Path(path).glob("**/*"):
        basename = file_name.name.lower()
        if basename.endswith(".yaml") or basename.endswith(".yml"):
            result.add(file_name)

    return result
