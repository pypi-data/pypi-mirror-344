"""
Report generation functionality
"""

import json
import yaml
from typing import Dict, Any, Union, Tuple
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class ReportGenerator:
    """Generates reports in various formats"""
    
    def __init__(self, scan_results: Dict[str, Any]):
        """Initialize with scan results"""
        self.results = scan_results
    
    def generate(self, format: str = "text") -> str:
        """Generate report in specified format"""
        if format == "text":
            return self._generate_text()
        elif format == "json":
            return self._generate_json()
        elif format == "yaml":
            return self._generate_yaml()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_text(self) -> str:
        """Generate human-readable text report"""
        table = Table(title="System Scan Report")
        table.add_column("Category", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="white")
        
        # Add system info
        table.add_row(
            "System Info",
            "OK",
            f"Host: {self.results['system_info']['hostname']}\n"
            f"OS: {self.results['system_info']['os']} {self.results['system_info']['os_version']}\n"
            f"Arch: {self.results['system_info']['architecture']}"
        )
        
        # Add scan results
        for category, result in self.results["scan_results"].items():
            if isinstance(result, dict):
                if result.get("status") == "error":
                    table.add_row(category, "ERROR", result.get("error", "Unknown error"))
                else:
                    table.add_row(category, "OK", str(result))
            elif isinstance(result, tuple):
                table.add_row(category, "OK", str(result))
            else:
                table.add_row(category, "OK", str(result))
        
        return str(table)
    
    def _generate_json(self) -> str:
        """Generate JSON report"""
        return json.dumps(self.results, indent=2)
    
    def _generate_yaml(self) -> str:
        """Generate YAML report"""
        return yaml.dump(self.results, default_flow_style=False) 