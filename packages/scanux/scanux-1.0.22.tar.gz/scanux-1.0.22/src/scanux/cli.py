"""
Command-line interface for scanux
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

from .core.scanner import SystemScanner
from .core.reporter import ReportGenerator

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="System security and performance scanner"
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

def format_issues(issues: List[Dict]) -> str:
    """Format issues for human-readable output."""
    if not issues:
        return "No issues found."

    output = []
    for issue in issues:
        output.append(f"[{issue['severity']}] {issue['title']}")
        output.append(f"  Description: {issue['description']}")
        if "recommendation" in issue:
            output.append(f"  Recommendation: {issue['recommendation']}")
        output.append("")
    return "\n".join(output)

def format_metrics(metrics: Dict) -> str:
    """Format metrics for human-readable output."""
    output = []
    for category, values in metrics.items():
        output.append(f"{category}:")
        for key, value in values.items():
            output.append(f"  {key}: {value}")
        output.append("")
    return "\n".join(output)

def main() -> int:
    """Main entry point."""
    args = parse_args()
    start_time = time.time()

    try:
        # Initialize scanner
        scanner = SystemScanner(args.modules)
        results = scanner.scan()
        
        # Generate report
        reporter = ReportGenerator(results)
        format = "json" if args.json else "yaml" if args.yaml else "text"
        report = reporter.generate(format)
        
        # Print report
        print(report)
        
        # Return appropriate exit code
        return 1 if any(
            result.get("status") == "error"
            for result in results["scan_results"].values()
        ) else 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 