# ansible-cleanup - Cleanup an Ansible project

[Ansible-cleanup](https://github.com/jamescherti/ansible-cleanup) provides command-line tools to find and remove unused playbooks, tasks, group variables, and host variables. It maintains a clean codebase by recursively scanning your Ansible repository and listing files that are safe to delete.

## Features

- Identify unused playbooks and tasks: Scans the repository to find all unused playbooks and tasks. It analyzes the codebase and determines which playbooks and tasks are no longer referenced or used.
- Find unused YAML files in group_vars and host_vars: Parses the "hosts" file, load all hosts and groups into a data structure. It then scans the `group_vars` and `host_vars` directories, identifying any YAML files that correspond to hosts or groups that no longer exist. This ensures that your variable files remain relevant and up-to-date.

## Installation

Here is how to install ansible-cleanup using [pip](https://pypi.org/project/pip/):

```bash
pip install --user git+https://github.com/jamescherti/ansible-cleanup
```

The pip command above will install the executable files in `~/.local/bin/`.

## Command Line Tools

### ansible-cleanup-unused-imports

This command acts as a static code analyzer for your Ansible execution paths. It takes a root playbook (or multiple playbooks) as an argument and recursively traces every `import_playbook`, `include_tasks`, `import_role`, and related Ansible includes. It then compares the files it successfully resolved against all the YAML files in your repository to find the orphans.

As infrastructure evolves, old task files and sub-playbooks are often disconnected from the main execution tree but are left behind in the repository. Manually tracing YAML includes across dozens of files is tedious and prone to human error. This command automates the discovery of dead code, ensuring your repository only contains files that are actually executed.

#### Usage:

Pass your primary entry-point playbook (e.g., `site.yml` or `main.yml`) as an argument. The script will output the absolute paths of any `.yml` or `.yaml` files that are not referenced anywhere in the execution tree.

```bash
$ ansible-cleanup-unused-imports site.yaml
/path/to/repo/playbooks/old_deployment_tasks.yml
/path/to/repo/playbooks/deprecated_setup.yaml

```

### ansible-cleanup-unused-vars

This command manages your variable definitions. It reads your local `hosts` inventory file and builds a comprehensive list of all active hosts and groups. It then cross-references this active list against the files located in your `host_vars` and `group_vars` directories to find files named after hosts or groups that are not defined in the inventory.

When servers are decommissioned or host groups are renamed, engineers frequently remove them from the `hosts` file but forget to delete the corresponding variable files in `host_vars/` or `group_vars/`. Over time, this leads to significant repository bloat and confusion over which variables are actually applied. This tool securely flags those forgotten files for deletion.

Execute the command in the directory containing your `hosts` file, `host_vars` directory, and `group_vars` directory. It requires no arguments.

#### Usage:

```bash
$ ansible-cleanup-unused-vars
/path/to/repo/host_vars/decommissioned-db-server-01.yml
/path/to/repo/group_vars/legacy-web-nodes.yaml

```

## License

Copyright (c) 2009-2026 [James Cherti](https://www.jamescherti.com)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Links

- [ansible-cleanup @GitHub](https://github.com/jamescherti/ansible-cleanup)
