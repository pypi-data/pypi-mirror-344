"""
Report generation functionality
"""

import json
import yaml
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

class ReportGenerator:
    """Generates reports in various formats"""
    
    def __init__(self, results: Dict[str, Any]):
        """Initialize with scan results"""
        self.results = results
    
    def generate(self, format: str = "text") -> str:
        """Generate report in specified format"""
        if format == "json":
            return self._generate_json()
        elif format == "yaml":
            return self._generate_yaml()
        else:
            return self._generate_text()
    
    def _generate_text(self) -> str:
        """Generate human-readable text report"""
        # Create main table
        table = Table(
            title="System Scan Results",
            box=box.ROUNDED,
            title_style="bold cyan",
            header_style="bold magenta",
            show_header=True,
            show_lines=True
        )
        
        # Add columns
        table.add_column("Module", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Metrics", style="green")
        table.add_column("Issues", style="red")
        
        # Add system info
        system_info = self.results["system_info"]
        table.add_row(
            "System",
            "[green]OK[/green]",
            f"OS: {system_info['os']} {system_info['os_version']}\n"
            f"Arch: {system_info['architecture']}\n"
            f"CPU: {system_info['cpu_count']} cores\n"
            f"Memory: {system_info['memory']['total'] / (1024**3):.1f} GB",
            ""
        )
        
        # Add scan results
        for module, result in self.results["scan_results"].items():
            if isinstance(result, tuple) and len(result) == 2:
                metrics, issues = result
                status = "[red]ERROR[/red]" if "error" in metrics else "[yellow]WARNING[/yellow]" if issues else "[green]OK[/green]"
                
                # Format metrics
                metrics_text = ""
                if isinstance(metrics, dict):
                    for key, value in metrics.items():
                        if key != "error":
                            metrics_text += f"{key}: {value}\n"
                
                # Format issues
                issues_text = ""
                if issues:
                    for issue in issues:
                        issues_text += f"• {issue}\n"
                
                table.add_row(
                    module.capitalize(),
                    status,
                    metrics_text.strip(),
                    issues_text.strip()
                )
            else:
                table.add_row(
                    module.capitalize(),
                    "[red]ERROR[/red]",
                    "Invalid result format",
                    str(result)
                )
        
        # Create final panel
        panel = Panel(
            table,
            title="[bold]Scanux System Scanner[/bold]",
            subtitle=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan"
        )
        
        return panel
    
    def _generate_json(self) -> str:
        """Generate JSON report"""
        return json.dumps(self.results, indent=2)
    
    def _generate_yaml(self) -> str:
        """Generate YAML report"""
        return yaml.dump(self.results, default_flow_style=False) 