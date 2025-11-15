# Ansible Role: Go language SDK

[![CI Tests](https://github.com/jepomeroy/ansible-role-golang/actions/workflows/ci.yml/badge.svg)](https://github.com/jepomeroy/ansible-role-golang/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/jepomeroy/ansible-role-golang/main/LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-CHANGELOG.md-blue.svg)](CHANGELOG.md)

Role to download and install the [Go language SDK](https://golang.org/).

## Why Use This Role?

- 🔐 **Pre-Configured Checksums**: Over 800 pre-verified SHA256 checksums for Go versions 1.2.2 through 1.24.10, eliminating manual verification steps
- 🏗️ **Multi-Architecture Support**: Built-in support for amd64, arm64, and armv6l architectures
- 🤖 **Automated Updates**: Weekly automated checks for new Go releases with automatic PR creation
- 🌍 **Cross-Platform Compatibility**: Tested and verified across Debian, Ubuntu, Rocky Linux, Fedora, and openSUSE distributions
- 🔄 **Version Flexibility**: Easily switch between Go versions or maintain multiple installations side-by-side
- ⚡ **Zero Manual Downloads**: Automatically fetches and verifies Go SDK packages from official mirrors
- ✅ **Idempotent & Safe**: Ansible-native implementation ensures safe, repeatable installations

## Requirements

- Ansible Core >= 2.12

- Linux Distribution (see tested versions below)

### Tested Linux Distributions

| Family | Distribution | Versions |
|--------|--------------|----------|
| Debian | Debian | Bullseye (11), Trixie (13) |
| Debian | Ubuntu | Jammy (22.04), Noble (24.04) |
| RedHat | Rocky Linux | 9 |
| RedHat | Fedora | 41 |
| SUSE | openSUSE | 15.6 |

> **Note**: Other versions are likely to work but have not been tested.

## Supported Go Versions

This role includes pre-configured checksums for the following Go SDK versions (latest patch for each minor version):

<!-- BEGIN GO VERSIONS -->
1.25.4, 1.24.10, 1.23.12, 1.22.12, 1.21.13, 1.20.14, 
1.19.13, 1.18.10, 1.17.13, 1.16.15, 1.15.15, 1.14.15, 
1.13.15, 1.12.17, 1.11.13, 1.10.8, 1.9.7, 1.8.7, 
1.7.6, 1.6.4, 1.5.4, 1.4.3, 1.3.3, 1.2.2
<!-- END GO VERSIONS -->

For a complete list of all supported versions and architectures, see the [vars/versions](vars/versions) directory.

## Role Variables

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# Go language SDK version number
golang_version: "1.22.6"

# Mirror to download the Go language SDK redistributable package from
golang_mirror: "https://storage.googleapis.com/golang"

# Base installation directory the Go language SDK distribution
golang_install_dir: "/opt/go/{{ golang_version }}"

# Directory to store files downloaded for Go language SDK installation
golang_download_dir: "{{ x_ansible_download_dir | default(ansible_facts.env.HOME + '/.ansible/tmp/downloads') }}"

# Location for GOPATH environment variable
golang_gopath:
```

## Advanced Configuration

The following role variable is dependent on the Go language SDK version; to use
a Go language SDK version **not pre-configured by this role** you must configure
the variable below:

```yaml
# SHA256 sum for the redistributable package (i.e. "go{{ golang_version }}.linux-amd64.tar.gz")
golang_redis_sha256sum: "6e3e9c949ab4695a204f74038717aa7b2689b1be94875899ac1b3fe42800ff82"
```

## Example Playbook

```yaml
- hosts: servers
  roles:
    - role: jepomeroy.golang
      golang_gopath: "$HOME/workspace-go"
```

**Note:** If you're migrating from the original GantSign role, simply update the role name from `gantsign.golang` to `jepomeroy.golang` in your playbooks.

## Role Facts

This role exports the following Ansible facts for use by other roles:

- `ansible_local.golang.general.version`
  - e.g. `1.7.3`

- `ansible_local.golang.general.home`
  - e.g. `/opt/golang/1.7.3`

## Development & Testing

This project uses the following tooling:

- [Molecule](http://molecule.readthedocs.io/) for orchestrating test scenarios
- [Testinfra](http://testinfra.readthedocs.io/) for testing the changes on the
  remote
- [pytest](http://docs.pytest.org/) the testing framework
- [Tox](https://tox.wiki/en/latest/) manages Python virtual
  environments for linting and testing
- [pip-tools](https://github.com/jazzband/pip-tools) for managing dependencies

A Visual Studio Code
[Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) is
provided for developing and testing this role.

## Acknowledgments

This project is wholly inspired by and based on the outstanding work of [GantSign Ltd.](https://github.com/gantsign) and [John Freeman](https://github.com/freemanjp). The original [ansible-role-golang](https://github.com/gantsign/ansible-role-golang) project provided the foundation and inspiration for this fork.

Special thanks to:

- **John Freeman** (freemanjp) - Original author and maintainer
- **GantSign Ltd.** - For their excellent Ansible roles and commitment to open source

For more quality Ansible roles from the original creators, visit [GantSign on Ansible Galaxy](https://galaxy.ansible.com/ui/standalone/namespaces/2463/).

## License

MIT

## Author Information

**Current Maintainer:**
JE Pomeroy

**Original Author:**
John Freeman
GantSign Ltd.
Company No. 06109112 (registered in England)
