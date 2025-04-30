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
        elif format == "html":
            return self._generate_html()
        else:
            return self._generate_text()
    
    def _format_network_data(self, data: Dict[str, Any]) -> str:
        """Format network data in a readable way"""
        output = []
        
        # Format open ports
        if 'open_ports' in data:
            output.append("Open Ports:")
            for port in data['open_ports']:
                output.append(f"  • {port['port']}/{port['protocol']}: {port['service']}")
        
        # Format firewall info
        if 'firewall' in data:
            firewall = data['firewall']
            output.append(f"\nFirewall Information:")
            output.append(f"  • Type: {firewall['type']}")
            output.append(f"  • Rules: {firewall['rules']}")
        
        # Format network interfaces
        if 'interfaces' in data:
            output.append("\nNetwork Interfaces:")
            for iface in data['interfaces']:
                output.append(f"  • {iface['name']}:")
                output.append(f"    - IP: {iface['ip']}")
                output.append(f"    - Netmask: {iface['netmask']}")
        
        return "\n".join(output)
    
    def _format_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format metrics in a readable way"""
        output = []
        
        for key, value in metrics.items():
            if key == 'error':
                continue
            elif key == 'network':
                output.append(self._format_network_data(value))
            elif isinstance(value, dict):
                output.append(f"{key.replace('_', ' ').title()}:")
                for subkey, subvalue in value.items():
                    output.append(f"  • {subkey.replace('_', ' ').title()}: {subvalue}")
            elif isinstance(value, list):
                output.append(f"{key.replace('_', ' ').title()}:")
                for item in value:
                    if isinstance(item, dict):
                        for k, v in item.items():
                            output.append(f"  • {k.replace('_', ' ').title()}: {v}")
                    else:
                        output.append(f"  • {item}")
            else:
                output.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(output)
    
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
        table.add_column("Details", style="green")
        
        # Add system info
        system_info = self.results["system_info"]
        table.add_row(
            "System",
            "[green]OK[/green]",
            "\n".join([
                f"OS: {system_info['os']} {system_info['os_version']}",
                f"Arch: {system_info['architecture']}",
                f"CPU: {system_info['cpu_count']} cores",
                f"Memory:",
                f"  • Total: {system_info['memory']['total']}",
                f"  • Available: {system_info['memory']['available']}",
                f"  • Used: {system_info['memory']['used']} ({system_info['memory']['percent']})"
            ])
        )
        
        # Add scan results
        for module, result in self.results["scan_results"].items():
            status = result["status"]
            status_text = {
                "ok": "[green]OK[/green]",
                "warning": "[yellow]WARNING[/yellow]",
                "error": "[red]ERROR[/red]"
            }.get(status, "[red]ERROR[/red]")
            
            # Format metrics
            metrics_text = self._format_metrics(result["metrics"])
            
            # Format issues
            issues_text = ""
            if result["issues"]:
                issues_text = "\nIssues Found:\n" + "\n".join(f"  • {issue}" for issue in result["issues"])
            
            table.add_row(
                module.capitalize(),
                status_text,
                metrics_text + issues_text
            )
        
        # Create final panel
        panel = Panel(
            table,
            title="[bold]Scanux System Scanner[/bold]",
            subtitle=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            border_style="cyan"
        )
        
        return panel
    
    def _generate_html(self) -> str:
        """Generate HTML report"""
        system_info = self.results["system_info"]
        scan_results = self.results["scan_results"]
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Scanux System Scan Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        .system-info {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .module {{
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .module h2 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .status {{
            font-weight: bold;
            padding: 3px 8px;
            border-radius: 3px;
            display: inline-block;
        }}
        .status-ok {{ background-color: #27ae60; color: white; }}
        .status-warning {{ background-color: #f1c40f; color: black; }}
        .status-error {{ background-color: #e74c3c; color: white; }}
        .metrics {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
        }}
        .issues {{
            margin: 10px 0;
            padding: 10px;
            background-color: #fff3cd;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Scanux System Scan Report</h1>
        
        <div class="system-info">
            <h2>System Information</h2>
            <p><strong>OS:</strong> {system_info['os']} {system_info['os_version']}</p>
            <p><strong>Architecture:</strong> {system_info['architecture']}</p>
            <p><strong>CPU:</strong> {system_info['cpu_count']} cores</p>
            <p><strong>Memory:</strong> {system_info['memory']['total'] / (1024**3):.1f} GB</p>
        </div>
        
        <div class="scan-results">
"""
        
        for module, result in scan_results.items():
            if isinstance(result, tuple) and len(result) == 2:
                metrics, issues = result
                if "error" in metrics:
                    status = "error"
                    status_class = "status-error"
                elif issues:
                    status = "warning"
                    status_class = "status-warning"
                else:
                    status = "ok"
                    status_class = "status-ok"
                
                html += f"""
            <div class="module">
                <h2>{module.capitalize()}</h2>
                <span class="status {status_class}">{status.upper()}</span>
                
                <div class="metrics">
                    <h3>Metrics</h3>
"""
                
                if isinstance(metrics, dict):
                    for key, value in metrics.items():
                        if key != "error":
                            html += f"                    <p><strong>{key}:</strong> {value}</p>\n"
                
                if issues:
                    html += """
                <div class="issues">
                    <h3>Issues</h3>
                    <ul>
"""
                    for issue in issues:
                        html += f"                        <li>{issue}</li>\n"
                    html += "                    </ul>\n                </div>\n"
                
                html += "            </div>\n"
        
        html += f"""
        </div>
        <div class="timestamp">
            Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_json(self) -> str:
        """Generate JSON report"""
        return json.dumps(self.results, indent=2)
    
    def _generate_yaml(self) -> str:
        """Generate YAML report"""
        return yaml.dump(self.results, default_flow_style=False) 