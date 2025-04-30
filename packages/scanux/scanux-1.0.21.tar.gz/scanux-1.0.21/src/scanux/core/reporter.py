"""
Enhanced reporter module for generating beautiful and detailed reports
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
from rich.box import DOUBLE, ROUNDED
from rich.style import Style
from rich.theme import Theme
from rich.layout import Layout
from rich.padding import Padding
from rich.columns import Columns

class ReportGenerator:
    """Generates beautifully formatted reports from scan results"""
    
    def __init__(self, results: Dict[str, Any]):
        """Initialize with scan results"""
        self.results = results
        self.console = Console(theme=Theme({
            "info": "cyan",
            "warning": "yellow",
            "error": "red",
            "success": "green",
            "header": "bold magenta",
            "metric": "blue",
            "title": "bold cyan",
            "subtitle": "italic cyan"
        }))
    
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
        """Generate a beautifully formatted text report"""
        from io import StringIO
        output = StringIO()
        temp_console = Console(file=output, force_terminal=True)
        
        # System Information Panel
        sys_info = self.results.get("system_info", {})
        if not isinstance(sys_info, dict):
            sys_info = {}
            
        header_table = Table(box=ROUNDED, show_header=False, border_style="bright_blue", padding=(0, 1))
        header_table.add_column("Key", style="bold cyan", width=15)
        header_table.add_column("Value", style="bright_white")
        
        header_items = [
            ("Hostname", sys_info.get("hostname", "Unknown")),
            ("OS", f"{sys_info.get('os', 'Unknown')} {sys_info.get('os_version', '')}".strip()),
            ("Architecture", sys_info.get("architecture", "Unknown")),
            ("CPU", f"{sys_info.get('processor', 'Unknown')} ({sys_info.get('cpu_count', 0)} cores)"),
            ("Memory", sys_info.get("memory", {}).get("total", "Unknown")),
            ("Scan Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ]
        
        for key, value in header_items:
            header_table.add_row(f" {key}", str(value))
        
        temp_console.print(Panel(
            header_table,
            title="[bold bright_blue]System Information[/]",
            border_style="bright_blue",
            padding=(1, 1),
            box=ROUNDED
        ))
        
        temp_console.print()  # Spacing
        
        # Module Results
        total_issues = 0
        scan_results = self.results.get("scan_results", {})
        
        for module_name, module_data in scan_results.items():
            if not isinstance(module_data, dict):
                continue
                
            module_table = Table(
                title=f"[bold bright_blue]{module_name.upper()} Module Results[/]",
                box=ROUNDED,
                show_header=True,
                header_style="bold bright_white",
                border_style="bright_blue",
                padding=(0, 1),
                collapse_padding=True,
                width=100
            )
            
            # Add columns with improved styling
            module_table.add_column("Category", style="bright_cyan", width=20)
            module_table.add_column("Status", justify="center", width=15)
            module_table.add_column("Details", style="bright_white", width=35)
            module_table.add_column("Recommendation", style="italic bright_white", width=30)
            
            has_data = False
            
            # Add metrics with improved formatting
            metrics = module_data.get("metrics", {})
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    if key == "error":
                        module_table.add_row(
                            Text("Error", style="bright_red"),
                            Text("⚠️", style="bright_red"),
                            Text(str(value), style="bright_red"),
                            Text("Check module configuration", style="bright_red")
                        )
                        has_data = True
                        continue
                        
                    has_data = True
                    if isinstance(value, dict):
                        details = "\n".join(f"{k}: {v}" for k, v in value.items())
                    else:
                        details = str(value)
                    
                    status = self._get_status_style(value)
                    recommendation = self._get_recommendation(key, value)
                    
                    module_table.add_row(
                        Text(key, style="bright_cyan"),
                        status,
                        Text(details, style="bright_white"),
                        Text(recommendation, style="italic bright_white")
                    )
            
            # Add issues with enhanced styling
            issues = module_data.get("issues", [])
            if isinstance(issues, list):
                total_issues += len(issues)
                for issue in issues:
                    has_data = True
                    if isinstance(issue, dict):
                        severity = issue.get("severity", "low")
                        symbol = self._get_severity_symbol(severity)
                        message = issue.get("message", "")
                        severity_style = self._get_severity_style(severity)
                        
                        module_table.add_row(
                            Text("Issue", style="bright_red"),
                            Text(symbol, style=severity_style),
                            Text(message, style=severity_style),
                            Text(self._get_issue_recommendation(severity, message), 
                                 style=f"italic {severity_style.color if severity_style.color else 'bright_white'}")
                        )
            
            # Add placeholder row if no data
            if not has_data:
                module_table.add_row(
                    "No data",
                    "✓",
                    "No issues or metrics found",
                    "System is healthy"
                )
            
            temp_console.print(module_table)
            temp_console.print()  # Spacing between tables
        
        # Summary Panel with enhanced styling
        summary_text = [
            "[bold bright_white]Total Issues Found:[/] " + str(total_issues),
            "[bold bright_white]Scan Completed:[/] " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        
        temp_console.print(Panel(
            "\n".join(summary_text),
            title="[bold bright_blue]Summary[/]",
            border_style="bright_blue",
            padding=(1, 1),
            box=ROUNDED
        ))
        
        return output.getvalue()
    
    def _generate_json(self) -> str:
        """Generate a JSON report"""
        return json.dumps(self.results, indent=2)
    
    def _generate_yaml(self) -> str:
        """Generate a YAML report"""
        return yaml.dump(self.results, default_flow_style=False)
    
    def _get_status_style(self, value) -> Text:
        """Get styled status text based on value"""
        if isinstance(value, (int, float)):
            if value > 90:
                return Text("⚠️ CRITICAL", style="bold bright_red")
            elif value > 75:
                return Text("⚠ WARNING", style="bold bright_yellow")
            elif value > 50:
                return Text("ℹ️ NOTICE", style="bold bright_blue")
            else:
                return Text("✓ OK", style="bold bright_green")
        elif isinstance(value, dict):
            return Text("ℹ️ INFO", style="bold bright_cyan")
        else:
            return Text("•", style="bright_white")
    
    def _get_severity_symbol(self, severity: str) -> str:
        """Get symbol for severity level"""
        return {
            "critical": "⚠️",
            "high": "⚠",
            "medium": "⚡",
            "low": "ℹ️",
            "info": "•"
        }.get(severity.lower(), "•")
    
    def _get_severity_style(self, severity: str) -> Style:
        """Get style for severity level"""
        return {
            "critical": Style(color="bright_red", bold=True),
            "high": Style(color="bright_yellow", bold=True),
            "medium": Style(color="bright_magenta"),
            "low": Style(color="bright_blue"),
            "info": Style(color="bright_cyan")
        }.get(severity.lower(), Style(color="bright_white"))
    
    def _get_recommendation(self, key: str, value) -> str:
        """Get recommendation based on metric key and value"""
        if isinstance(value, (int, float)):
            if value > 90:
                return "Immediate action required"
            elif value > 75:
                return "Action recommended"
            elif value > 50:
                return "Monitor closely"
            else:
                return "No action needed"
        return "Review if needed"
    
    def _get_issue_recommendation(self, severity: str, message: str) -> str:
        """Get recommendation based on issue severity"""
        return {
            "critical": "Fix immediately",
            "high": "Fix as soon as possible",
            "medium": "Plan to fix soon",
            "low": "Fix when convenient",
            "info": "Review if needed"
        }.get(severity.lower(), "Review if needed") 