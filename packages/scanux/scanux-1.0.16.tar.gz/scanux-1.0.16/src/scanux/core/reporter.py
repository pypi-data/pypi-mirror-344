"""
Report generation functionality for scan results
"""

import json
import yaml
from typing import Dict, Any
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

class ReportGenerator:
    """Generates formatted reports from scan results"""
    
    def __init__(self, results: Dict[str, Any]):
        """Initialize with scan results"""
        self.results = results
        self.console = Console()
    
    def generate(self, format_type: str = "text") -> str:
        """Generate a report in the specified format"""
        if format_type == "text":
            return self._generate_text()
        elif format_type == "json":
            return self._generate_json()
        elif format_type == "yaml":
            return self._generate_yaml()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_text(self) -> str:
        """Generate a human-readable text report"""
        # Create a simple table with basic borders
        table = Table(
            show_header=True,
            header_style="bold blue",
            box=box.ASCII,
            title="System Status Report",
            padding=(0, 2),
            show_edge=True
        )
        
        # Add columns
        table.add_column("Component")
        table.add_column("Status")
        
        # System Information
        if "system_info" in self.results:
            info = self.results["system_info"]
            table.add_row(
                "Operating System",
                f"{info.get('os', 'Unknown')} {info.get('os_version', '')}"
            )
            table.add_row(
                "Architecture",
                info.get('architecture', 'Unknown')
            )
            table.add_row(
                "CPU",
                f"{info.get('cpu_count', 0)} cores"
            )
            
            # Memory info
            if 'memory' in info:
                mem = info['memory']
                table.add_row(
                    "Memory",
                    f"Total: {mem.get('total', '?')}\n"
                    f"Used: {mem.get('used', '?')} ({mem.get('percent', '?')})\n"
                    f"Available: {mem.get('available', '?')}"
                )
        
        # Disk Usage
        if "metrics" in self.results:
            metrics = self.results["metrics"]
            for key, value in metrics.items():
                if key.startswith("disk_usage_"):
                    mount = key.replace("disk_usage_", "")
                    table.add_row(
                        f"Disk ({mount})",
                        f"Total: {value['total']}\n"
                        f"Used: {value['used']} ({value['percent']}%)\n"
                        f"Free: {value['free']}"
                    )
        
        # CPU Usage
        if "metrics" in self.results and "cpu" in self.results["metrics"]:
            cpu = self.results["metrics"]["cpu"]
            table.add_row(
                "CPU Usage",
                f"{cpu['percent']}% (Cores: {cpu['count']})"
            )
        
        # Issues
        if self.results.get("issues"):
            table.add_section()
            table.add_row("Issues Found", "")
            for issue in self.results["issues"]:
                severity = issue.get("severity", "unknown").upper()
                message = issue.get("message", "")
                table.add_row(
                    severity,
                    message
                )
        
        # Create the final output
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        panel = Panel(
            table,
            title=f"[bold cyan]Scan Report - {timestamp}[/bold cyan]",
            border_style="cyan"
        )
        
        # Render to string
        with self.console.capture() as capture:
            self.console.print(panel)
        return capture.get()
    
    def _generate_json(self) -> str:
        """Generate a JSON report"""
        return json.dumps(self.results, indent=2)
    
    def _generate_yaml(self) -> str:
        """Generate a YAML report"""
        return yaml.dump(self.results, default_flow_style=False) 