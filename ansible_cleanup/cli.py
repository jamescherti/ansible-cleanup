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
"""Centralized command line interface for ansible-cleanup."""

from __future__ import annotations

import argparse
import collections.abc
import sys

from ansible_cleanup.cli_find_unused_tasks import \
    command_line_interface as imports_cli
from ansible_cleanup.cli_find_unused_vars import \
    command_line_interface as vars_cli


def main(argv: collections.abc.Sequence[str] | None = None) -> int:
    """Parse arguments and route execution to the correct cleanup module."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Utilities for cleaning up Ansible projects."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand for imports
    imports_parser: argparse.ArgumentParser = subparsers.add_parser(
        "imports",
        help="Detect unused tasks and imports within the project",
    )
    imports_parser.add_argument(
        "playbooks",
        nargs="+",
        help="One or more playbook YAML files to parse",
    )

    # Subcommand for variables
    subparsers.add_parser(
        "vars",
        help="Detect unused variables within the project",
    )

    args: argparse.Namespace = parser.parse_args(argv)

    if args.command == "imports":
        return imports_cli(args.playbooks)
    if args.command == "vars":
        return vars_cli()

    return 0


if __name__ == "__main__":
    sys.exit(main())
