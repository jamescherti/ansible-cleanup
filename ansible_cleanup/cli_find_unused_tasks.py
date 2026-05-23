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
"""Find unused tasks."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import ansible

from .find_imports import FindImports


def find_all_yaml_files() -> set[Path]:
    """Find YAML files in the repo, excluding variable and role directories."""
    all_yaml_files: set[Path] = set()
    for file_name in Path(".").glob("**/*"):
        basename: str = file_name.name.lower()
        file_path: Path = file_name.absolute()

        if "host_vars" in file_path.parts or \
                "group_vars" in file_path.parts or \
                "roles" in file_path.parts:
            continue

        if basename.endswith(".yaml") or basename.endswith(".yml"):
            all_yaml_files.add(file_path)

    return all_yaml_files


def find_yaml_files_that_are_imported(files: list[str]) \
        -> Optional[FindImports]:
    """Parse a list of playbooks and trace all imported YAML files."""
    playbook = None
    for item in files:
        playbook_path: Path = Path(item).absolute()

        if playbook:
            if playbook_path not in playbook.ignore_files:
                new_playbook = FindImports(file_name=playbook_path,
                                           base_dir=playbook_path.parent)
                new_playbook.merge(playbook)
                new_playbook.find_imports()
                playbook = new_playbook
        else:
            playbook = FindImports(file_name=playbook_path,
                                   base_dir=playbook_path.parent)
            playbook.find_imports()

    return playbook


def command_line_interface(playbooks: list[str]) -> int:
    """Execute the command line interface logic for finding unused tasks."""
    if not playbooks:
        print("Usage: ansible-cleanup imports <playbook.yaml>",
              file=sys.stderr)
        return 1

    all_yaml_files: set[Path] = find_all_yaml_files()

    try:
        playbook: Optional[FindImports] = find_yaml_files_that_are_imported(
            playbooks)
    except ansible.errors.AnsibleFileNotFound as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    if not playbook:
        print("Nothing to do.")
        return 1

    # Show unused tasks/playbooks
    all_yaml_files -= playbook.get_all_files()
    for file_name in sorted(all_yaml_files):
        print(file_name)

    # print()

    # Show imports
    # for item in playbook.get_all_files():
    #     print(item)
    # if playbook.failed:
    #     for item in sorted(playbook.failed):
    #         print(f"[FAILED] {item}")
    #     print()
    # return 0

    # if all_yaml_files:
    #     print("Detailed imports:")
    #     print("-----------------")
    #     for import_file in sorted(playbook.imports.keys()):
    #         categories = playbook.imports[import_file]
    #         print(import_file)
    #         print("-" * len(str(import_file)))
    #         for category, imported_files in categories.items():
    #             if not imported_files:
    #                 continue
    #
    #             print(f"{category}:")
    #             for imported_file in imported_files:
    #                 print(f"    - {imported_file}")
    #             print()
    #
    # if playbook.roles:
    #     print("Roles:")
    #     print("-----")
    #     for item in sorted(playbook.roles):
    #         print(f"  - {item}")
    #     print()

    return 0
