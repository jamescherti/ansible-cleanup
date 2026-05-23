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
from ansible_cleanup.find_imports import FindImports

DATA_PATH = Path(".").joinpath("tests", "data", "find_imports")
PLAYBOOK_PATH = DATA_PATH.joinpath("playbook.yml").absolute()
PLAYBOOK_DIR = PLAYBOOK_PATH.parent.absolute()


@pytest.fixture
def playbook_roles():
    return {'role1', 'role2', 'role3', 'role4', 'role5', 'role6'}


@pytest.fixture
def playbook_imports() -> dict:
    return {
        PLAYBOOK_PATH: {
            'playbooks': {PLAYBOOK_DIR.joinpath('inc_playbook1.yml'),
                          PLAYBOOK_DIR.joinpath('inc_playbook2.yml')},
            'tasks': {PLAYBOOK_DIR.joinpath('tasks1.yml'),
                      PLAYBOOK_DIR.joinpath('tasks2.yaml'),
                      PLAYBOOK_DIR.joinpath('tasks3.yml'),
                      PLAYBOOK_DIR.joinpath('tasks4.yaml')},
            'vars': {PLAYBOOK_DIR.joinpath('group_vars/vault.yml')}}
    }


@pytest.fixture
def find_imports():
    cleanup_playbook = FindImports(file_name=PLAYBOOK_PATH,
                                   base_dir=PLAYBOOK_PATH.parent,
                                   recursive=False)
    cleanup_playbook.find_imports()
    return cleanup_playbook


@pytest.fixture
def find_imports_recursive():
    cleanup_playbook = FindImports(file_name=PLAYBOOK_PATH,
                                   base_dir=PLAYBOOK_PATH.parent,
                                   recursive=True)
    cleanup_playbook.find_imports()
    return cleanup_playbook


@pytest.fixture
def playbook_categories(playbook_imports):
    return playbook_imports[PLAYBOOK_PATH]


def test_parse_playbook_host_name(find_imports: FindImports):
    assert find_imports.ansible_data.data[0]["hosts"] == "the_host"


def test_merge(find_imports: FindImports):
    new_find_imports = FindImports(file_name=PLAYBOOK_PATH,
                                   base_dir=PLAYBOOK_PATH.parent,
                                   recursive=False)
    new_find_imports.merge(find_imports)
    assert new_find_imports.imports == find_imports.imports
    assert new_find_imports.ignore_files == find_imports.ignore_files
    assert new_find_imports.roles == find_imports.roles
    assert new_find_imports.failed == find_imports.failed


def test_get_all_files(find_imports: FindImports, playbook_categories):
    assert find_imports.get_all_files() == \
        (playbook_categories["vars"] |
         playbook_categories["tasks"] |
         {PLAYBOOK_PATH} |
         playbook_categories["playbooks"])


def test_parse_playbook_import(find_imports: FindImports,
                               playbook_imports,
                               playbook_roles):
    assert find_imports.ansible_data.data[0]["hosts"] == "the_host"
    assert find_imports.roles == playbook_roles
    assert find_imports.imports == playbook_imports


def test_parse_playbook_import_recursive(find_imports_recursive,
                                         playbook_categories,
                                         playbook_roles):
    assert find_imports_recursive.roles == playbook_roles
    assert find_imports_recursive.failed == set()
    assert find_imports_recursive.ignore_files == \
        {PLAYBOOK_DIR.joinpath('group_vars/vault.yml')} | \
        {PLAYBOOK_PATH}
    assert find_imports_recursive.get_all_files() == \
        (playbook_categories["vars"] | playbook_categories["tasks"] |
         playbook_categories["playbooks"] |
         {PLAYBOOK_PATH} |
         {PLAYBOOK_DIR.joinpath('tasks5.yml'),
          PLAYBOOK_DIR.joinpath('tasks6.yaml'),
          PLAYBOOK_DIR.joinpath('inc_playbook3.yml')})
