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
"""Ansible variables (host_vars and group_vars)."""

from __future__ import annotations

import os
from pathlib import Path

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

from .helpers import find_yaml_files


class AnsibleVars:
    def __init__(self,
                 hosts_file: os.PathLike,
                 host_vars_dir: os.PathLike = Path('host_vars'),
                 group_vars_dir: os.PathLike = Path('group_vars')):
        self.hosts_file = Path(hosts_file)
        self.base_dir = Path(self.hosts_file).parent

        self.host_vars_dir = Path(host_vars_dir)
        if not self.host_vars_dir.is_absolute():
            self.host_vars_dir = self.base_dir.joinpath(self.host_vars_dir)

        self.group_vars_dir = Path(group_vars_dir)
        if not self.group_vars_dir.is_absolute():
            self.group_vars_dir = self.base_dir.joinpath(self.group_vars_dir)

        # Load hosts file
        data_loader = DataLoader()
        self.inventory_manager = InventoryManager(
            loader=data_loader,
            sources=[str(self.hosts_file)])

    def get_hosts(self) -> set[str]:
        return set(map(str, self.inventory_manager.get_hosts()))

    def get_groups(self) -> set[str]:
        return set(self.inventory_manager.get_groups_dict().keys())

    def find_unused_group_vars(self) -> set[Path]:
        yaml_files = find_yaml_files(self.group_vars_dir)
        for group in self.get_groups():
            yaml_files -= {Path(self.group_vars_dir).joinpath(f"{group}.yml")}
            yaml_files -= {Path(self.group_vars_dir).joinpath(f"{group}.yaml")}
        return yaml_files

    def find_unused_host_vars(self) -> set[Path]:
        yaml_files = find_yaml_files(self.host_vars_dir)
        for host in self.get_hosts():
            yaml_files -= {Path(self.host_vars_dir).joinpath(f"{host}.yml")}
            yaml_files -= {Path(self.host_vars_dir).joinpath(f"{host}.yaml")}

        return yaml_files
