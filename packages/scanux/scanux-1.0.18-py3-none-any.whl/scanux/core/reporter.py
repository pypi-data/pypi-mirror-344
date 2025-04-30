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
from rich.box import DOUBLE_EDGE
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
        # Create a string buffer to capture the output
        from io import StringIO
        output = StringIO()
        temp_console = Console(file=output, force_terminal=True)
        
        # Create main layout
        layout = Layout()
        layout.split(
            Layout(name="header"),
            Layout(name="body", ratio=3)
        )
        
        # Create header with system information
        sys_info = self.results.get("system", {})
        if isinstance(sys_info, dict):
            sys_info = sys_info.get("system_info", {})
        else:
            sys_info = {}
            
        header_table = Table(box=DOUBLE_EDGE, show_header=False, border_style="cyan")
        header_table.add_column("Key", style="bold cyan")
        header_table.add_column("Value", style="white")
        
        header_items = [
            ("Hostname", sys_info.get("hostname", "Unknown")),
            ("OS", f"{sys_info.get('os', 'Unknown')} {sys_info.get('os_version', '')}"),
            ("Architecture", sys_info.get("architecture", "Unknown")),
            ("CPU", sys_info.get("processor", "Unknown")),
            ("Scan Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ]
        
        for key, value in header_items:
            header_table.add_row(key, value)
        
        # Create tables for each module
        tables = []
        total_issues = 0
        
        for module_name, module_data in self.results.items():
            if not isinstance(module_data, dict):
                continue
                
            # Module table with custom styling
            module_table = Table(
                title=f"[title]{module_name.upper()} Module Results[/title]",
                box=DOUBLE_EDGE,
                show_header=True,
                header_style="bold magenta",
                border_style="blue",
                title_style="bold cyan",
                padding=(0, 1)
            )
            
            # Add columns with custom styles
            module_table.add_column("Category", style="cyan")
            module_table.add_column("Status", justify="center")
            module_table.add_column("Details", style="white")
            module_table.add_column("Recommendation", style="italic")
            
            # Add metrics
            metrics = module_data.get("metrics", {})
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    if isinstance(value, dict):
                        details = "\n".join(f"{k}: {v}" for k, v in value.items())
                    else:
                        details = str(value)
                    
                    status = self._get_status_style(value)
                    recommendation = self._get_recommendation(key, value)
                    
                    module_table.add_row(
                        key,
                        status,
                        Text(details, overflow="fold"),
                        recommendation
                    )
            
            # Add issues with warning symbols and colors
            issues = module_data.get("issues", [])
            if isinstance(issues, list):
                total_issues += len(issues)
                for issue in issues:
                    if isinstance(issue, dict):
                        severity = issue.get("severity", "low")
                        symbol = self._get_severity_symbol(severity)
                        message = issue.get("message", "")
                        
                        module_table.add_row(
                            "Issue",
                            Text(symbol, style=self._get_severity_style(severity)),
                            Text(message, style=self._get_severity_style(severity)),
                            self._get_issue_recommendation(severity, message)
                        )
            
            tables.append(module_table)
        
        # Render the report
        temp_console.print(Panel(
            header_table,
            title="[title]System Information[/title]",
            border_style="cyan",
            padding=(1, 2)
        ))
        
        temp_console.print()  # Add spacing
        
        # Render module tables in columns for better layout
        for table in tables:
            temp_console.print(table)
            temp_console.print()  # Add spacing between tables
        
        # Add footer with summary
        footer = Panel(
            f"Total Issues Found: {total_issues}\nScan Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan",
            title="[title]Summary[/title]",
            padding=(1, 2)
        )
        temp_console.print(footer)
        
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
                return Text("⚠️ CRITICAL", style="red bold")
            elif value > 75:
                return Text("⚠ WARNING", style="yellow bold")
            elif value > 50:
                return Text("ℹ️ NOTICE", style="blue")
            else:
                return Text("✓ OK", style="green")
        elif isinstance(value, dict):
            return Text("ℹ️ INFO", style="cyan")
        else:
            return Text("•", style="white")
    
    def _get_severity_symbol(self, severity: str) -> str:
        """Get symbol for severity level"""
        return {
            "high": "🔴",
            "medium": "🟡",
            "low": "🔵",
        }.get(severity.lower(), "⚪")
    
    def _get_severity_style(self, severity: str) -> Style:
        """Get style for severity level"""
        return {
            "high": "red bold",
            "medium": "yellow",
            "low": "blue",
        }.get(severity.lower(), "white")
    
    def _get_recommendation(self, key: str, value) -> str:
        """Generate recommendation based on metric"""
        if isinstance(value, (int, float)):
            if value > 90:
                return "Immediate action required"
            elif value > 75:
                return "Monitor closely"
            elif value > 50:
                return "Consider optimization"
        return "No action needed"
    
    def _get_issue_recommendation(self, severity: str, message: str) -> str:
        """Generate recommendation based on issue"""
        if severity == "high":
            return "Address immediately"
        elif severity == "medium":
            return "Plan to resolve soon"
        else:
            return "Monitor and review" 