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


from .ansible_vars import AnsibleVars


def command_line_interface():
    ansible_vars = AnsibleVars("hosts")
    for item in ansible_vars.find_unused_host_vars():
        print(item)
    for item in ansible_vars.find_unused_group_vars():
        print(item)


if __name__ == '__main__':
    command_line_interface()
