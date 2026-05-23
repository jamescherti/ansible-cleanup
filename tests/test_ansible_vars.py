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
from ansible_cleanup.ansible_vars import AnsibleVars

DATA_PATH = Path(".").joinpath("tests", "data", "ansible_vars")
HOSTS_FILE = DATA_PATH.joinpath("hosts")


@pytest.fixture
def ansible_vars():
    return AnsibleVars(HOSTS_FILE)


def test_ansible_vars(ansible_vars: AnsibleVars):
    assert ansible_vars.get_hosts() == {"host1",
                                        "host2",
                                        "host3"}


def test_ansible_groups(ansible_vars: AnsibleVars):
    assert ansible_vars.get_groups() == {'all', 'ungrouped',
                                         'group1', 'group2'}


def test_unused_host_vars(ansible_vars: AnsibleVars):
    assert ansible_vars.find_unused_host_vars() == \
        {DATA_PATH.joinpath("host_vars", "host4.yml"),
         DATA_PATH.joinpath("host_vars", "host5.yaml")}


def test_unused_group_vars(ansible_vars: AnsibleVars):
    assert ansible_vars.find_unused_group_vars() == {
        DATA_PATH.joinpath("group_vars", "group3.yaml"),
        DATA_PATH.joinpath("group_vars", "group4.yml"),
        DATA_PATH.joinpath("group_vars", "group5.yaml"),
    }
