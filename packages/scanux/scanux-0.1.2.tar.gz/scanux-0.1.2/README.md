# scanux

A system scanning tool for Linux and Windows systems that:
- Scans connected users
- Identifies suspicious behavior
- Analyzes command history
- Generates reports in multiple formats

## Features

- **User Scanning**: Lists all currently connected users with their details
- **Suspicious Behavior Detection**: Identifies processes with high CPU/memory usage
- **Command History Analysis**: Analyzes recent command history
- **Multiple Report Formats**: Supports JSON, Markdown, and HTML output formats
- **Cross-Platform**: Works on both Linux and Windows systems

## Installation

```bash
pip install scanux
```

## Usage

Basic usage:
```bash
scanux
```

Generate a report in a specific format:
```bash
scanux --format json
scanux --format markdown
scanux --format html
```

Save report to a file:
```bash
scanux --format json --output report.json
scanux --format markdown --output report.md
scanux --format html --output report.html
```

## Report Contents

The generated report includes:
- System information (platform, release, version, machine)
- List of connected users
- Suspicious behavior detection
- Recent command history

## Requirements

- Python 3.6 or higher
- psutil
- rich
- click
- python-dateutil

## License

MIT License 