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


import sys
from pathlib import Path
from typing import Any

from ansible import constants as C

from .ansible_vars import AnsibleVars


def command_line_interface() -> None:
    """Find unused variables and print them to standard output."""
    # pylint: disable=no-member
    inventory_sources: Any = C.DEFAULT_HOST_LIST
    hosts_file: str = "hosts"

    if isinstance(inventory_sources, str) and inventory_sources:
        hosts_file = inventory_sources
    elif isinstance(inventory_sources, (list, tuple)) and inventory_sources:
        hosts_file = str(inventory_sources[0])

    hosts_path: Path = Path(hosts_file)
    if not hosts_path.exists():
        print(
            f"Error: Inventory file or directory does not exist: {hosts_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    ansible_vars: AnsibleVars = AnsibleVars(hosts_file)

    for item in ansible_vars.find_unused_host_vars():
        print(item)

    for item in ansible_vars.find_unused_group_vars():
        print(item)


if __name__ == '__main__':
    command_line_interface()
