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

import os
import sys
from pathlib import Path

from .find_imports import FindImports


def find_all_yaml_files():
    all_yaml_files = set()
    for file_name in Path(".").glob("**/*"):
        basename = file_name.name.lower()
        file_name = file_name.absolute()

        if "/host_vars/" in str(file_name) or \
                "/group_vars/" in str(file_name) or \
                "/roles/" in str(file_name):
            continue

        if basename.endswith(".yaml") or basename.endswith(".yml"):
            all_yaml_files.add(file_name)

    return all_yaml_files


def find_yaml_files_that_are_imported(files: list[os.PathLike]):
    playbook = None
    for playbook_path in files:
        playbook_path = Path(playbook_path).absolute()
        if not playbook_path.is_file():
            raise FileNotFoundError(f"File not found: {playbook_path}")

        playbook_path = Path(playbook_path)
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


def command_line_interface():
    try:
        sys.argv[1]
    except IndexError:
        print(f"Usage: {sys.argv[0]} <playbook.yaml>", file=sys.stderr)
        sys.exit(1)

    all_yaml_files = find_all_yaml_files()

    playbook = find_yaml_files_that_are_imported(sys.argv[1:])
    if not playbook:
        print("Nothing to do.")
        sys.exit(1)

    # Show unused tasks/playbooks
    all_yaml_files -= playbook.get_all_files()
    for file_name in sorted(all_yaml_files):
        print(file_name)

    print()
    sys.exit(0)

    # Show imports
    # for item in playbook.get_all_files():
    #     print(item)
    # if playbook.failed:
    #     for item in sorted(playbook.failed):
    #         print(f"[FAILED] {item}")
    #     print()
    # sys.exit(0)

    if all_yaml_files:
        print("Detailed imports:")
        print("-----------------")
        for file_name in sorted(playbook.imports.keys()):
            categories = playbook.imports[file_name]
            print(file_name)
            print("-" * len(str(file_name)))
            for category, imported_files in categories.items():
                if not imported_files:
                    continue

                print(f"{category}:")
                for file_name in imported_files:
                    print(f"    - {file_name}")
                print()

    if playbook.roles:
        print("Roles:")
        print("-----")
        for item in sorted(playbook.roles):
            print(f"  - {item}")
        print()


if __name__ == '__main__':
    command_line_interface()
