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
        # Create the main table with a more visible border style
        table = Table(
            title="System Security and Performance Scan Report",
            show_header=True,
            header_style="bold magenta",
            box=box.DOUBLE,
            padding=(0, 1),
            expand=True
        )
        
        # Add columns with proper spacing
        table.add_column("Category", style="cyan", width=15)
        table.add_column("Metric", style="green", width=20)
        table.add_column("Value", style="yellow", width=40)
        
        # System Information
        if "system_info" in self.results:
            system_info = self.results["system_info"]
            for key, value in system_info.items():
                if isinstance(value, dict):
                    # Handle nested dictionaries (like memory)
                    formatted_value = ", ".join(f"{k}: {v}" for k, v in value.items())
                else:
                    formatted_value = str(value)
                table.add_row(
                    "System",
                    key.replace("_", " ").title(),
                    formatted_value
                )
        
        # Add a separator
        table.add_section()
        
        # Resource Usage
        if "metrics" in self.results:
            metrics = self.results["metrics"]
            
            # Disk Usage
            for key, value in metrics.items():
                if key.startswith("disk_usage_"):
                    mount = key.replace("disk_usage_", "")
                    table.add_row(
                        "Disk",
                        f"Mount {mount}",
                        f"Total: {value['total']}\nUsed: {value['used']} ({value['percent']}%)\nFree: {value['free']}"
                    )
            
            # Memory Usage
            if "memory" in metrics:
                memory = metrics["memory"]
                table.add_row(
                    "Memory",
                    "RAM Usage",
                    f"Total: {memory['total']}\nUsed: {memory['used']} ({memory['percent']}%)\nAvailable: {memory['available']}"
                )
            
            # CPU Usage
            if "cpu" in metrics:
                cpu = metrics["cpu"]
                table.add_row(
                    "CPU",
                    "Usage",
                    f"{cpu['percent']}% (Cores: {cpu['count']})"
                )
        
        # Add a separator before issues
        table.add_section()
        
        # Issues Section
        if self.results.get("issues"):
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
            title=f"[cyan]Scan completed at {timestamp}[/cyan]",
            border_style="blue",
            padding=(1, 1)
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