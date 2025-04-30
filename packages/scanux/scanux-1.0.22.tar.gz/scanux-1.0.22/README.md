# Scanux

A system security and performance scanner that checks for security vulnerabilities, performance issues, and network security problems.

## Features

- Security scanning
  - File permissions
  - User accounts
  - System services
  - Security configurations
- Performance scanning
  - CPU usage
  - Memory usage
  - Disk usage
  - Process analysis
- Network scanning
  - Open ports
  - Listening services
  - Network connections
  - Firewall status

## Installation

```bash
pip install scanux
```

## Usage

Run a full system scan:

```bash
scanux
```

Show only issues:

```bash
scanux --issues-only
```

Get JSON output:

```bash
scanux --json
```

Get YAML output:

```bash
scanux --yaml
```

Run specific modules:

```bash
scanux --modules system security
```

## Return Codes

- 0: No issues found
- 1: Issues found or error occurred

## Requirements

- Python 3.8 or higher
- psutil
- python-nmap
- netifaces
- rich
- pyyaml

## License

MIT 