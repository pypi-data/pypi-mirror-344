#!/usr/bin/env python3
"""
Command-line interface for scanux
"""

import argparse
import json
import sys
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.table import Table
from rich.prompt import Confirm
from rich import print as rprint

from .core.scanner import SystemScanner
from .core.reporter import ReportGenerator

console = Console()

def check_dependencies() -> bool:
    """Check if required system dependencies are installed."""
    try:
        subprocess.run(['nmap', '--version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print(Panel(
            "[red]Error: nmap is not installed on your system.[/red]\n\n"
            "Please install nmap using your system's package manager:\n"
            "- Ubuntu/Debian: [yellow]sudo apt-get install nmap[/yellow]\n"
            "- CentOS/RHEL: [yellow]sudo yum install nmap[/yellow]\n"
            "- macOS: [yellow]brew install nmap[/yellow]",
            title="Dependency Error",
            border_style="red"
        ))
        return False

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="System security and performance scanner"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "yaml"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (optional)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--yaml",
        action="store_true",
        help="Output results in YAML format",
    )
    parser.add_argument(
        "--issues-only",
        action="store_true",
        help="Show only issues, skip metrics",
    )
    parser.add_argument(
        "--modules",
        nargs="+",
        choices=["system", "security", "performance", "network"],
        default=["system", "security", "performance", "network"],
        help="Specify which modules to run",
    )
    return parser.parse_args()

def main() -> int:
    """Main entry point."""
    if not check_dependencies():
        sys.exit(1)

    args = parse_args()
    
    # Create scanner
    scanner = SystemScanner(args.modules)
    
    # Show progress if not quiet
    if not args.quiet:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning system...", total=None)
            results = scanner.scan()
            progress.update(task, completed=True)
    else:
        results = scanner.scan()
    
    # Generate report
    reporter = ReportGenerator(results)
    report = reporter.generate(args.format)
    
    # Output report
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
    else:
        if args.format == "text":
            console.print(report)
        else:
            print(report)
    
    # Return appropriate exit code
    return 1 if any(
        result.get("status") == "error"
        for result in results["scan_results"].values()
    ) else 0

if __name__ == "__main__":
    sys.exit(main()) 