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
        # Create the main table
        table = Table(title="System Security and Performance Scan Report", show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Metric", style="green")
        table.add_column("Value", style="yellow")
        
        # System Information
        if "system_info" in self.results:
            table.add_row(
                "System",
                "Operating System",
                f"{self.results['system_info'].get('os', 'Unknown')}"
            )
            table.add_row(
                "System",
                "Architecture",
                f"{self.results['system_info'].get('architecture', 'Unknown')}"
            )
        
        # Disk Usage
        for key, value in self.results.get("metrics", {}).items():
            if key.startswith("disk_usage_"):
                mount = key.replace("disk_usage_", "")
                table.add_row(
                    "Disk",
                    f"Mount {mount}",
                    f"Total: {value['total']}, Used: {value['used']} ({value['percent']}%)"
                )
        
        # Memory Usage
        if "memory" in self.results.get("metrics", {}):
            memory = self.results["metrics"]["memory"]
            table.add_row(
                "Memory",
                "RAM Usage",
                f"Total: {memory['total']}, Used: {memory['used']} ({memory['percent']}%)"
            )
        
        # CPU Usage
        if "cpu" in self.results.get("metrics", {}):
            cpu = self.results["metrics"]["cpu"]
            table.add_row(
                "CPU",
                "Usage",
                f"{cpu['percent']}% (Cores: {cpu['count']})"
            )
        
        # Issues Section
        if self.results.get("issues"):
            table.add_section()
            for issue in self.results["issues"]:
                severity = issue.get("severity", "unknown")
                style = {
                    "high": "red",
                    "medium": "yellow",
                    "low": "green"
                }.get(severity, "white")
                
                table.add_row(
                    Text("Issue", style=style),
                    Text(severity.upper(), style=style),
                    Text(issue["message"], style=style)
                )
        
        # Create a panel with the table and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        panel = Panel(
            table,
            title=f"Scan completed at {timestamp}",
            border_style="blue"
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