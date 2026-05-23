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
# pylint: disable=redefined-outer-name
"""Test the ansible_cleanup module."""

from pathlib import Path

import pytest
from ansible_cleanup.helpers import (AnsibleConfig, existing_file_with_ext,
                                     find_yaml_files)

DATA_PATH = Path(".").joinpath("tests", "data", "helpers")


def test_ansible_config():
    ansible_config = AnsibleConfig(DATA_PATH.joinpath("ansible.cfg"))
    assert ansible_config.get('defaults', 'host_vars') == "new_host_var"
    assert ansible_config.get('defaults', 'group_vars') == "new_group_var"


def test_existing_file_with_ext():
    base_path = DATA_PATH.joinpath("group_vars", "group4")
    assert existing_file_with_ext(
        base_path, [".bmp", ".yml", ".yaml"],
    ).name == "group4.yml"


def test_existing_file_with_ext_not_found():
    base_path = DATA_PATH.joinpath("group_vars", "group200")
    with pytest.raises(FileNotFoundError):
        existing_file_with_ext(base_path, [".bmp", ".yml", ".yaml"])


def test_find_yaml_files():
    assert find_yaml_files(DATA_PATH) == \
        set(DATA_PATH.glob("**/*")) - \
        {DATA_PATH.joinpath("group_vars"),
         DATA_PATH.joinpath("host_vars"),
         DATA_PATH.joinpath("ansible.cfg"),
         DATA_PATH.joinpath("hosts")}
