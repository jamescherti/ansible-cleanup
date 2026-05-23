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
"""Static code analyzer that parses Ansible imports and includes."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Union

import ansible
from ansible.parsing.dataloader import DataLoader
# pylint: disable=no-name-in-module
from ansible.parsing.yaml.objects import (AnsibleMapping, AnsibleSequence,
                                          AnsibleUnicode)


class InvalidFileFormat(Exception):
    """The file format is not valid."""


class AnsibleData:
    """Represents the loaded Ansible YAML data."""

    def __init__(self, file_name: os.PathLike) -> None:
        """Initialize the AnsibleData instance with a file."""
        self.file_name = Path(file_name)
        self._data_loader = DataLoader()
        self.data = self._data_loader.load_from_file(str(file_name))


class FindImports:
    """Finds all imports and includes recursively in an Ansible file."""

    def __init__(self,
                 file_name: os.PathLike,
                 base_dir: os.PathLike,
                 recursive: bool = True,
                 ignore_files: Union[set[Path], None] = None) -> None:
        """Initialize FindImports with the target file and base directory."""
        self._needles = {
            # Roles
            "import_role": "roles",
            "ansible.builtin.include_role": "roles",
            "include_role": "roles",
            "ansible.builtin.import_role": "roles",
            # Playbooks
            "import_playbook": "playbooks",
            "ansible.builtin.import_playbook": "playbooks",
            # Tasks
            "import_tasks": "tasks",
            "ansible.builtin.import_tasks": "tasks",
            "include_tasks": "tasks",
            "ansible.builtin.include_tasks": "tasks",
            # Vars
            "include_vars": "vars",
            "ansible.builtin.include_vars": "vars",
        }

        self.recursive = recursive
        self.ansible_data = AnsibleData(file_name)

        self.file_name = Path(file_name).absolute()
        self.base_dir = Path(base_dir).absolute()

        self.ignore_files: set[Path] = set()
        if ignore_files:
            self.ignore_files |= set(map(Path, ignore_files))
        self.ignore_files.add(self.file_name)
        self.failed: set[Path] = set()  # Failed to load these files

        # Init imports
        self.imports: dict[Path, dict[str, set[Union[str, Path]]]] = {}
        self.roles: set[str] = set()
        try:
            self.imports[self.file_name]
        except KeyError:
            self.imports[self.file_name] = {}

        for _, category in self._needles.items():
            if category == "roles":
                continue

            try:
                self.imports[self.file_name][category]
            except KeyError:
                self.imports[self.file_name][category] = set()

    def find_imports(self) -> None:
        """Execute the search for Ansible imports and includes."""
        self._find_imports_recursive(self.ansible_data.data)
        if not self.recursive:
            return

        failed = self.failed.copy()
        ignore_files = self.ignore_files.copy()
        reserved_files = self.get_all_files() | self.ignore_files

        files_to_parse = self.get_all_files() - self.ignore_files
        for file_name in files_to_parse:
            file_name = self.base_dir.joinpath(file_name)
            try:
                imports = FindImports(
                    file_name=file_name,
                    base_dir=self.base_dir,
                    recursive=True,
                    ignore_files=reserved_files,
                )
            except ansible.parsing.vault.AnsibleVaultError:
                # Ignore vault files
                reserved_files.add(file_name)
                ignore_files.add(file_name)
                failed -= {file_name}
            except ansible.errors.AnsibleFileNotFound:
                reserved_files.add(file_name)
                failed.add(file_name)
            else:
                imports.find_imports()
                self.merge(imports)

        self.failed = failed
        self.ignore_files = ignore_files

    def get_all_files(self) -> set[Path]:
        """Return a set of all file paths discovered during the search."""
        result: set[Path] = set()
        for file_name, categories in self.imports.items():
            result.add(Path(file_name))
            for _, files in categories.items():
                for item in files:
                    result.add(Path(item))
        return result

    def merge(self, find_imports: 'FindImports') -> None:
        """Merge the imports and failures from another FindImports instance."""
        self.failed |= find_imports.failed
        self.ignore_files |= find_imports.ignore_files
        self.roles |= find_imports.roles
        for file_name, categories in find_imports.imports.items():
            if file_name not in self.imports:
                self.imports[file_name] = {}

            for category, files in categories.items():
                if category not in self.imports[file_name]:
                    self.imports[file_name][category] = set()

                self.imports[file_name][category] |= files

    def _ansible_func_to_category(self, ansible_func: str) -> str:
        """Ansible function name to category.

        For example: 'import_role' -> returns 'roles'.

        """
        for ansible_func2, generic_name in self._needles.items():
            if ansible_func == ansible_func2:
                return generic_name
        return ""

    def _is_supported_ansible_type(self, data: Any) -> bool:
        # Using isinstance instead of exact type() matching catches
        # Ansible's internal subclassed wrappers like _AnsibleTaggedStr
        return isinstance(data, (type(None), bool, int, float, str, bytes))

    def _add_import(self, category: str,
                    file_name: Union[str, os.PathLike]) -> None:
        if category == "roles":
            self.roles.add(str(file_name))
        else:
            file_name = self.base_dir.joinpath(file_name)
            self.imports[self.file_name][category].add(file_name)

    def _find_imports_recursive(self, data: Any) -> None:
        error = False
        error_data = None
        if isinstance(data, (AnsibleSequence, list)):
            self._parse_ansible_sequence(data)
        elif isinstance(data, (AnsibleMapping, dict)):
            (error_data, error) = self._parse_ansible_mapping(data)
        elif not self._is_supported_ansible_type(data):
            error_data = data
            error = True

        if error:
            err_str = (f"Invalid data in {self.ansible_data.file_name}: "
                       f"{type(error_data)}: {error_data}")
            raise InvalidFileFormat(err_str)

    def _parse_ansible_sequence(
            self, data: Union[AnsibleSequence, list]) -> None:
        for item in data:
            self._find_imports_recursive(item)

    def _parse_ansible_mapping(
            self, data: Union[AnsibleMapping, dict]) -> tuple[Any, bool]:
        error_data = data
        error = False
        for ansible_func, sub_data in data.items():
            if ansible_func == "roles":
                self._parse_playbook_roles(sub_data)
                continue

            if ansible_func == "tags":
                continue  # Ignore tags

            if self._parse_ansible_func(ansible_func, sub_data):
                # Added
                continue

            # Other
            if isinstance(sub_data, (AnsibleMapping,
                          dict, AnsibleSequence, list)):
                self._find_imports_recursive(sub_data)
                continue

            if self._is_supported_ansible_type(sub_data):
                continue

            error_data = sub_data
            error = True

        return (error_data, error)

    def _parse_ansible_func(self, ansible_func: str,
                            data: Union[AnsibleMapping, AnsibleSequence,
                                        dict, list]) -> bool:
        """Parse an Ansible function/module."""
        category = self._ansible_func_to_category(ansible_func)
        if category:
            self._add_import(category,
                             data["name"] if category == "roles" else data)
            return True

        return False

    def _parse_playbook_roles(self, data: Union[AnsibleMapping,
                                                AnsibleSequence,
                                                dict, list]) -> None:
        """Parse the roles of a Playbook.

        Example:
            roles:
              - role1
              - {"role": "role2"}

        """
        for roles_data in data:
            category = "roles"
            if not isinstance(roles_data, str):
                try:
                    roles_data = roles_data["role"]
                except KeyError:
                    roles_data = roles_data["name"]

            self._add_import(category, roles_data)
