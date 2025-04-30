import os
import sys
import platform
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import json
import psutil
from pathlib import Path

console = Console()

def get_connected_users():
    """Get list of connected users"""
    users = []
    if platform.system() == "Linux":
        # Get logged in users
        for user in psutil.users():
            users.append({
                "name": user.name,
                "terminal": user.terminal,
                "host": user.host,
                "started": datetime.fromtimestamp(user.started).isoformat(),
                "pid": user.pid
            })
    elif platform.system() == "Windows":
        # Get logged in users on Windows
        for user in psutil.users():
            users.append({
                "name": user.name,
                "terminal": user.terminal,
                "host": user.host,
                "started": datetime.fromtimestamp(user.started).isoformat(),
                "pid": user.pid
            })
    return users

def check_suspicious_behavior():
    """Check for suspicious behavior"""
    suspicious = []
    
    # Check for unusual processes
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            process = proc.info
            # Example checks (customize based on your needs)
            if process['cpu_percent'] > 80:  # High CPU usage
                suspicious.append({
                    "type": "high_cpu",
                    "process": process['name'],
                    "pid": process['pid'],
                    "user": process['username'],
                    "cpu_percent": process['cpu_percent']
                })
            if process['memory_percent'] > 80:  # High memory usage
                suspicious.append({
                    "type": "high_memory",
                    "process": process['name'],
                    "pid": process['pid'],
                    "user": process['username'],
                    "memory_percent": process['memory_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return suspicious

def analyze_command_history():
    """Analyze command history"""
    history = []
    home_dir = str(Path.home())
    
    if platform.system() == "Linux":
        history_file = os.path.join(home_dir, ".bash_history")
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    history.append(line.strip())
    
    return history

def generate_report(users, suspicious, history, output_format="markdown"):
    """Generate report in specified format"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "connected_users": users,
        "suspicious_behavior": suspicious,
        "command_history": history
    }
    
    if output_format == "json":
        return json.dumps(report, indent=2)
    elif output_format == "markdown":
        return generate_markdown_report(report)
    elif output_format == "html":
        return generate_html_report(report)
    return None

def generate_markdown_report(report):
    """Generate markdown report"""
    md = f"# System Scan Report\n\n"
    md += f"Generated on: {report['timestamp']}\n\n"
    
    md += "## System Information\n"
    md += f"- Platform: {report['system']['platform']}\n"
    md += f"- Release: {report['system']['release']}\n"
    md += f"- Version: {report['system']['version']}\n"
    md += f"- Machine: {report['system']['machine']}\n\n"
    
    md += "## Connected Users\n"
    for user in report['connected_users']:
        md += f"- {user['name']} ({user['terminal']}) from {user['host']}\n"
    md += "\n"
    
    md += "## Suspicious Behavior\n"
    for item in report['suspicious_behavior']:
        md += f"- {item['type']}: {item['process']} (PID: {item['pid']})\n"
    md += "\n"
    
    md += "## Recent Command History\n"
    for cmd in report['command_history'][-10:]:  # Show last 10 commands
        md += f"- `{cmd}`\n"
    
    return md

def generate_html_report(report):
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Scan Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2 {{ color: #333; }}
            .section {{ margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>System Scan Report</h1>
        <p>Generated on: {report['timestamp']}</p>
        
        <div class="section">
            <h2>System Information</h2>
            <table>
                <tr><th>Platform</th><td>{report['system']['platform']}</td></tr>
                <tr><th>Release</th><td>{report['system']['release']}</td></tr>
                <tr><th>Version</th><td>{report['system']['version']}</td></tr>
                <tr><th>Machine</th><td>{report['system']['machine']}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Connected Users</h2>
            <table>
                <tr><th>User</th><th>Terminal</th><th>Host</th></tr>
    """
    
    for user in report['connected_users']:
        html += f"""
                <tr>
                    <td>{user['name']}</td>
                    <td>{user['terminal']}</td>
                    <td>{user['host']}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Suspicious Behavior</h2>
            <table>
                <tr><th>Type</th><th>Process</th><th>PID</th></tr>
    """
    
    for item in report['suspicious_behavior']:
        html += f"""
                <tr>
                    <td>{item['type']}</td>
                    <td>{item['process']}</td>
                    <td>{item['pid']}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Recent Command History</h2>
            <table>
                <tr><th>Command</th></tr>
    """
    
    for cmd in report['command_history'][-10:]:
        html += f"""
                <tr><td><code>{cmd}</code></td></tr>
        """
    
    html += """
            </table>
        </div>
    </body>
    </html>
    """
    
    return html

@click.command()
@click.option('--format', '-f', type=click.Choice(['json', 'markdown', 'html']), 
              default='markdown', help='Output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def main(format, output):
    """System scanning tool for Linux and Windows systems"""
    console.print(Panel.fit("🔍 Starting system scan...", title="scanux"))
    
    # Collect data
    users = get_connected_users()
    suspicious = check_suspicious_behavior()
    history = analyze_command_history()
    
    # Generate report
    report = generate_report(users, suspicious, history, format)
    
    # Output report
    if output:
        with open(output, 'w') as f:
            f.write(report)
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        console.print(report)

if __name__ == '__main__':
    main() 