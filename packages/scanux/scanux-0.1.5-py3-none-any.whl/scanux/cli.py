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
import socket
import subprocess
import re
import uuid
import getpass
import time
import yaml
import netifaces
import iptc
import dbus
import selinux
from typing import Dict, List, Any, Optional
import hashlib
import grp
import pwd
import stat
import glob
import tarfile
import gzip
import shutil
from collections import defaultdict

# Constants for suspicious patterns
SUSPICIOUS_COMMANDS = [
    r'rm\s+-rf',
    r'chmod\s+777',
    r'wget\s+http',
    r'curl\s+http',
    r'nc\s+-l',
    r'nmap',
    r'hydra',
    r'john',
    r'aircrack',
    r'ssh\s+-R',
    r'ssh\s+-D',
    r'ssh\s+-L',
    r'nc\s+-e',
    r'python\s+-c',
    r'perl\s+-e',
    r'bash\s+-i',
    r'chattr\s+\+i',
    r'chattr\s+-i',
    r'iptables\s+-F',
    r'iptables\s+-P',
    r'ufw\s+disable',
    r'systemctl\s+stop',
    r'service\s+stop',
    r'killall',
    r'pkill',
    r'kill\s+-9',
    r'crontab\s+-r',
    r'crontab\s+-l\s+>\s+',
    r'passwd\s+root',
    r'useradd',
    r'userdel',
    r'groupadd',
    r'groupdel',
    r'chown\s+root',
    r'chmod\s+4755',
    r'chmod\s+u\+s',
    r'chmod\s+g\+s',
    r'chmod\s+o\+w',
    r'chmod\s+o\+x',
    r'chmod\s+o\+r',
    r'chmod\s+o\+w',
    r'chmod\s+o\+x',
    r'chmod\s+o\+r',
    r'chmod\s+o\+w',
    r'chmod\s+o\+x',
    r'chmod\s+o\+r',
]

SUSPICIOUS_PATHS = [
    '/tmp/',
    '/dev/shm/',
    '/var/tmp/',
    '/var/run/',
    '/proc/',
    '/sys/',
    '/root/',
    '/etc/cron.d/',
    '/etc/cron.hourly/',
    '/etc/cron.daily/',
    '/etc/cron.weekly/',
    '/etc/cron.monthly/',
    '/var/spool/cron/',
    '/var/spool/cron/crontabs/',
]

SUSPICIOUS_PORTS = [
    22,  # SSH
    23,  # Telnet
    80,  # HTTP
    443, # HTTPS
    3306, # MySQL
    5432, # PostgreSQL
    27017, # MongoDB
    6379, # Redis
    8080, # HTTP Alt
    8443, # HTTPS Alt
]

console = Console()

def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information"""
    system_info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "platform_release": platform.release(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "python_version": platform.python_version(),
        "system_time": datetime.now().isoformat(),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
        "system_uptime": time.time() - psutil.boot_time(),
        "cpu_count": {
            "physical": psutil.cpu_count(logical=False),
            "logical": psutil.cpu_count(logical=True)
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "free": psutil.virtual_memory().free,
            "percent": psutil.virtual_memory().percent
        },
        "swap": {
            "total": psutil.swap_memory().total,
            "used": psutil.swap_memory().used,
            "free": psutil.swap_memory().free,
            "percent": psutil.swap_memory().percent
        }
    }
    return system_info

def get_disk_info() -> List[Dict[str, Any]]:
    """Get detailed disk information"""
    disk_info = []
    for partition in psutil.disk_partitions(all=True):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "opts": partition.opts,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent
            })
        except (PermissionError, OSError):
            continue
    return disk_info

def get_network_info() -> Dict[str, Any]:
    """Get comprehensive network information"""
    network_info = {
        "interfaces": {},
        "connections": [],
        "dns": {
            "nameservers": [],
            "hosts": {}
        }
    }
    
    # Get network interfaces
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            network_info["interfaces"][interface] = []
            for addr in addrs:
                network_info["interfaces"][interface].append({
                    "family": addr.family.name,
                    "address": addr.address,
                    "netmask": addr.netmask,
                    "broadcast": addr.broadcast
                })
    except (psutil.AccessDenied, PermissionError) as e:
        network_info["interfaces"] = {"error": f"Permission denied: {str(e)}"}
    
    # Get network connections (optional on macOS)
    try:
        for conn in psutil.net_connections():
            try:
                network_info["connections"].append({
                    "family": conn.family.name,
                    "type": conn.type.name,
                    "local_addr": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    "remote_addr": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    "status": conn.status if hasattr(conn, 'status') else None,
                    "pid": conn.pid
                })
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
    except (psutil.AccessDenied, PermissionError) as e:
        network_info["connections"] = {"error": f"Permission denied: {str(e)}"}
    
    # Get DNS information
    try:
        if platform.system() == 'Darwin':  # macOS
            result = subprocess.run(['scutil', '--dns'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'nameserver' in line:
                    nameserver = line.split()[-1]
                    if nameserver not in network_info["dns"]["nameservers"]:
                        network_info["dns"]["nameservers"].append(nameserver)
        else:  # Linux
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.startswith('nameserver'):
                        network_info["dns"]["nameservers"].append(line.split()[1])
    except (FileNotFoundError, PermissionError, subprocess.SubprocessError) as e:
        network_info["dns"] = {"error": f"Failed to get DNS info: {str(e)}"}
    
    return network_info

def get_process_info() -> List[Dict[str, Any]]:
    """Get detailed process information"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 
                                   'create_time', 'cmdline', 'status', 'nice', 'num_threads']):
        try:
            process = proc.info
            processes.append({
                "pid": process['pid'],
                "name": process['name'],
                "username": process['username'],
                "cpu_percent": process['cpu_percent'],
                "memory_percent": process['memory_percent'],
                "create_time": datetime.fromtimestamp(process['create_time']).isoformat(),
                "cmdline": process['cmdline'],
                "status": process['status'],
                "nice": process['nice'],
                "num_threads": process['num_threads']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def get_user_info() -> List[Dict[str, Any]]:
    """Get detailed user information"""
    users = []
    for user in psutil.users():
        users.append({
            "name": user.name,
            "terminal": user.terminal,
            "host": user.host,
            "started": datetime.fromtimestamp(user.started).isoformat(),
            "pid": user.pid
        })
    return users

def get_security_info() -> Dict[str, Any]:
    """Get security-related information"""
    security_info = {
        "sudoers": [],
        "cron_jobs": [],
        "ssh_keys": [],
        "open_ports": [],
        "firewall_status": None
    }
    
    # Check sudoers file
    try:
        if platform.system() == 'Darwin':  # macOS
            with open('/private/etc/sudoers', 'r') as f:
                security_info["sudoers"] = f.readlines()
        else:  # Linux
            with open('/etc/sudoers', 'r') as f:
                security_info["sudoers"] = f.readlines()
    except (FileNotFoundError, PermissionError) as e:
        security_info["sudoers"] = [f"Permission denied: {str(e)}"]
    
    # Check cron jobs
    try:
        if platform.system() == 'Darwin':  # macOS
            for user in psutil.users():
                try:
                    cron_path = f"/usr/lib/cron/tabs/{user.name}"
                    if os.path.exists(cron_path):
                        with open(cron_path, 'r') as f:
                            security_info["cron_jobs"].extend(f.readlines())
                except (FileNotFoundError, PermissionError):
                    continue
        else:  # Linux
            for user in psutil.users():
                try:
                    cron_path = f"/var/spool/cron/crontabs/{user.name}"
                    if os.path.exists(cron_path):
                        with open(cron_path, 'r') as f:
                            security_info["cron_jobs"].extend(f.readlines())
                except (FileNotFoundError, PermissionError):
                    continue
    except (FileNotFoundError, PermissionError) as e:
        security_info["cron_jobs"] = [f"Permission denied: {str(e)}"]
    
    # Check SSH keys
    try:
        ssh_dir = os.path.expanduser("~/.ssh")
        if os.path.exists(ssh_dir):
            for file in os.listdir(ssh_dir):
                if file.endswith('.pub'):
                    with open(os.path.join(ssh_dir, file), 'r') as f:
                        security_info["ssh_keys"].append(f.read().strip())
    except (FileNotFoundError, PermissionError) as e:
        security_info["ssh_keys"] = [f"Permission denied: {str(e)}"]
    
    # Check open ports (optional on macOS)
    try:
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN':
                security_info["open_ports"].append({
                    "port": conn.laddr.port,
                    "address": conn.laddr.ip,
                    "protocol": conn.type.name
                })
    except (psutil.AccessDenied, PermissionError) as e:
        security_info["open_ports"] = [f"Permission denied: {str(e)}"]
    
    # Check firewall status
    try:
        if platform.system() == 'Darwin':  # macOS
            result = subprocess.run(['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getglobalstate'], 
                                  capture_output=True, text=True)
            security_info["firewall_status"] = result.stdout
        elif platform.system() == 'Linux':
            result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
            security_info["firewall_status"] = result.stdout
        elif platform.system() == 'Windows':
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                  capture_output=True, text=True)
            security_info["firewall_status"] = result.stdout
    except (FileNotFoundError, subprocess.SubprocessError, PermissionError) as e:
        security_info["firewall_status"] = f"Failed to get firewall status: {str(e)}"
    
    return security_info

def get_suspicious_behavior() -> Dict[str, Any]:
    """Check for suspicious behavior"""
    suspicious = {
        "high_cpu_processes": [],
        "high_memory_processes": [],
        "unusual_ports": [],
        "suspicious_commands": []
    }
    
    # Check for high CPU usage
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
        try:
            process = proc.info
            if process['cpu_percent'] > 80:  # Threshold for high CPU usage
                suspicious["high_cpu_processes"].append({
                    "pid": process['pid'],
                    "name": process['name'],
                    "username": process['username'],
                    "cpu_percent": process['cpu_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Check for high memory usage
    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
        try:
            process = proc.info
            if process['memory_percent'] > 80:  # Threshold for high memory usage
                suspicious["high_memory_processes"].append({
                    "pid": process['pid'],
                    "name": process['name'],
                    "username": process['username'],
                    "memory_percent": process['memory_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Check for unusual ports
    unusual_ports = [22, 80, 443, 3306, 5432, 27017]  # Common ports
    for conn in psutil.net_connections():
        try:
            if conn.status == 'LISTEN' and conn.laddr.port not in unusual_ports:
                suspicious["unusual_ports"].append({
                    "port": conn.laddr.port,
                    "address": conn.laddr.ip,
                    "protocol": conn.type.name
                })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    
    # Check for suspicious commands in history
    suspicious_patterns = [
        r'rm\s+-rf',
        r'chmod\s+777',
        r'wget\s+http',
        r'curl\s+http',
        r'nc\s+-l',
        r'nmap',
        r'hydra',
        r'john',
        r'aircrack'
    ]
    
    try:
        history_file = os.path.expanduser("~/.bash_history")
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                for line in f:
                    for pattern in suspicious_patterns:
                        if re.search(pattern, line):
                            suspicious["suspicious_commands"].append(line.strip())
                            break
    except (FileNotFoundError, PermissionError):
        pass
    
    return suspicious

def get_selinux_status() -> Dict[str, Any]:
    """Get SELinux status and configuration"""
    try:
        return {
            "enabled": selinux.is_selinux_enabled(),
            "enforced": selinux.security_getenforce(),
            "policy": selinux.selinux_getpolicytype()[1],
            "context": selinux.getcon()[1],
        }
    except Exception as e:
        return {"error": str(e)}

def get_systemd_services() -> Dict[str, Any]:
    """Get systemd services status"""
    services = {
        "active": [],
        "failed": [],
        "masked": [],
    }
    try:
        bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')
        
        for unit in manager.ListUnits():
            name, description, load_state, active_state, sub_state, following, unit_path, job_id, job_type = unit
            if active_state == 'active':
                services["active"].append(name)
            elif active_state == 'failed':
                services["failed"].append(name)
            elif load_state == 'masked':
                services["masked"].append(name)
    except Exception as e:
        return {"error": str(e)}
    return services

def get_iptables_rules() -> List[Dict[str, Any]]:
    """Get iptables rules"""
    rules = []
    try:
        for table in ['filter', 'nat', 'mangle']:
            table_obj = iptc.Table(table)
            for chain in table_obj.chains:
                for rule in chain.rules:
                    rules.append({
                        "table": table,
                        "chain": chain.name,
                        "rule": str(rule),
                        "target": rule.target.name if rule.target else None,
                    })
    except Exception as e:
        return [{"error": str(e)}]
    return rules

def get_network_interfaces() -> Dict[str, Any]:
    """Get detailed network interface information"""
    interfaces = {}
    try:
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            interfaces[interface] = {
                "mac": addrs.get(netifaces.AF_LINK, [{}])[0].get('addr'),
                "ipv4": [addr['addr'] for addr in addrs.get(netifaces.AF_INET, [])],
                "ipv6": [addr['addr'] for addr in addrs.get(netifaces.AF_INET6, [])],
                "netmask": [addr.get('netmask') for addr in addrs.get(netifaces.AF_INET, [])],
                "broadcast": [addr.get('broadcast') for addr in addrs.get(netifaces.AF_INET, [])],
            }
    except Exception as e:
        return {"error": str(e)}
    return interfaces

def get_suspicious_files() -> List[Dict[str, Any]]:
    """Find suspicious files in the system"""
    suspicious_files = []
    try:
        for path in SUSPICIOUS_PATHS:
            if os.path.exists(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        try:
                            stat_info = os.stat(full_path)
                            if stat.S_ISUID & stat_info.st_mode or stat.S_ISGID & stat_info.st_mode:
                                suspicious_files.append({
                                    "path": full_path,
                                    "permissions": oct(stat_info.st_mode)[-3:],
                                    "owner": pwd.getpwuid(stat_info.st_uid).pw_name,
                                    "group": grp.getgrgid(stat_info.st_gid).gr_name,
                                    "size": stat_info.st_size,
                                    "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                                })
                        except Exception:
                            continue
    except Exception as e:
        return [{"error": str(e)}]
    return suspicious_files

def get_cron_jobs() -> Dict[str, Any]:
    """Get all cron jobs"""
    cron_jobs = {
        "system": [],
        "users": defaultdict(list)
    }
    try:
        # System cron jobs
        for cron_file in glob.glob('/etc/cron.d/*'):
            try:
                with open(cron_file, 'r') as f:
                    cron_jobs["system"].extend(f.readlines())
            except Exception:
                continue

        # User cron jobs
        for user in pwd.getpwall():
            try:
                user_cron = subprocess.check_output(['crontab', '-l', '-u', user.pw_name], 
                                                 stderr=subprocess.DEVNULL).decode()
                if user_cron:
                    cron_jobs["users"][user.pw_name].extend(user_cron.splitlines())
            except Exception:
                continue
    except Exception as e:
        return {"error": str(e)}
    return cron_jobs

def get_sudoers() -> Dict[str, Any]:
    """Get sudoers configuration"""
    sudoers = {
        "file": [],
        "sudoers.d": []
    }
    try:
        # Main sudoers file
        with open('/etc/sudoers', 'r') as f:
            sudoers["file"] = f.readlines()

        # Sudoers.d directory
        for sudo_file in glob.glob('/etc/sudoers.d/*'):
            try:
                with open(sudo_file, 'r') as f:
                    sudoers["sudoers.d"].append({
                        "file": sudo_file,
                        "content": f.readlines()
                    })
            except Exception:
                continue
    except Exception as e:
        return {"error": str(e)}
    return sudoers

def get_ssh_config() -> Dict[str, Any]:
    """Get SSH configuration"""
    ssh_config = {
        "server_config": [],
        "authorized_keys": defaultdict(list),
        "known_hosts": []
    }
    try:
        # SSH server config
        with open('/etc/ssh/sshd_config', 'r') as f:
            ssh_config["server_config"] = f.readlines()

        # Authorized keys
        for user in pwd.getpwall():
            auth_keys_file = os.path.join(user.pw_dir, '.ssh', 'authorized_keys')
            if os.path.exists(auth_keys_file):
                try:
                    with open(auth_keys_file, 'r') as f:
                        ssh_config["authorized_keys"][user.pw_name] = f.readlines()
                except Exception:
                    continue

        # Known hosts
        known_hosts_file = os.path.expanduser('~/.ssh/known_hosts')
        if os.path.exists(known_hosts_file):
            with open(known_hosts_file, 'r') as f:
                ssh_config["known_hosts"] = f.readlines()
    except Exception as e:
        return {"error": str(e)}
    return ssh_config

def get_package_info() -> Dict[str, Any]:
    """Get installed package information"""
    packages = {
        "dpkg": [],
        "rpm": [],
        "pip": []
    }
    try:
        # Debian/Ubuntu packages
        if os.path.exists('/usr/bin/dpkg'):
            dpkg_output = subprocess.check_output(['dpkg', '-l']).decode()
            packages["dpkg"] = dpkg_output.splitlines()

        # RPM packages
        if os.path.exists('/usr/bin/rpm'):
            rpm_output = subprocess.check_output(['rpm', '-qa']).decode()
            packages["rpm"] = rpm_output.splitlines()

        # Python packages
        pip_output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode()
        packages["pip"] = pip_output.splitlines()
    except Exception as e:
        return {"error": str(e)}
    return packages

def get_system_logs() -> Dict[str, Any]:
    """Get system logs"""
    logs = {
        "auth": [],
        "syslog": [],
        "kern": [],
        "messages": []
    }
    try:
        log_files = {
            "auth": '/var/log/auth.log',
            "syslog": '/var/log/syslog',
            "kern": '/var/log/kern.log',
            "messages": '/var/log/messages'
        }
        
        for log_type, log_file in log_files.items():
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        logs[log_type] = f.readlines()[-1000:]  # Last 1000 lines
                except Exception:
                    continue
    except Exception as e:
        return {"error": str(e)}
    return logs

def generate_report(output_format: str = "markdown") -> str:
    """Generate comprehensive system report"""
    console.print(Panel.fit("🔍 Starting comprehensive Linux system scan...", title="scanux"))
    
    try:
        # Collect all data
        data = {
            "timestamp": datetime.now().isoformat(),
            "system_info": get_system_info(),
            "disk_info": get_disk_info(),
            "network_info": {
                "interfaces": get_network_interfaces(),
                "connections": get_network_info()["connections"],
                "iptables": get_iptables_rules()
            },
            "security_info": {
                "selinux": get_selinux_status(),
                "sudoers": get_sudoers(),
                "ssh": get_ssh_config(),
                "suspicious_files": get_suspicious_files(),
                "cron_jobs": get_cron_jobs()
            },
            "process_info": get_process_info(),
            "user_info": get_user_info(),
            "services": get_systemd_services(),
            "packages": get_package_info(),
            "logs": get_system_logs(),
            "suspicious_behavior": get_suspicious_behavior()
        }
        
        if output_format == "json":
            return json.dumps(data, indent=2)
        elif output_format == "markdown":
            return generate_markdown_report(data)
        elif output_format == "html":
            return generate_html_report(data)
        return None
    except Exception as e:
        error_msg = f"Error during scan: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        if output_format == "json":
            return json.dumps({"error": error_msg}, indent=2)
        return error_msg

def generate_markdown_report(data: Dict[str, Any]) -> str:
    """Generate markdown report"""
    md = f"# System Scan Report\n\n"
    md += f"Generated on: {data['timestamp']}\n\n"
    
    # System Information
    md += "## System Information\n"
    md += f"- Platform: {data['system_info']['platform']} {data['system_info']['platform_version']}\n"
    md += f"- Architecture: {data['system_info']['architecture']}\n"
    md += f"- Hostname: {data['system_info']['hostname']}\n"
    md += f"- FQDN: {data['system_info']['fqdn']}\n"
    md += f"- Python Version: {data['system_info']['python_version']}\n"
    md += f"- Boot Time: {data['system_info']['boot_time']}\n"
    md += f"- Uptime: {data['system_info']['system_uptime']:.2f} seconds\n"
    md += f"- CPU Count: {data['system_info']['cpu_count']['physical']} physical, {data['system_info']['cpu_count']['logical']} logical\n"
    md += f"- Memory: {data['system_info']['memory']['used'] / (1024**3):.2f}GB used ({data['system_info']['memory']['percent']}%)\n"
    md += f"- Swap: {data['system_info']['swap']['used'] / (1024**3):.2f}GB used ({data['system_info']['swap']['percent']}%)\n\n"
    
    # Disk Information
    md += "## Disk Information\n"
    for disk in data['disk_info']:
        md += f"### {disk['device']} ({disk['mountpoint']})\n"
        md += f"- Filesystem: {disk['fstype']}\n"
        md += f"- Options: {disk['opts']}\n"
        md += f"- Usage: {disk['used'] / (1024**3):.2f}GB used ({disk['percent']}%)\n"
        md += f"- Free: {disk['free'] / (1024**3):.2f}GB\n\n"
    
    # Network Information
    md += "## Network Information\n"
    md += "### Interfaces\n"
    for interface, addrs in data['network_info']['interfaces'].items():
        md += f"#### {interface}\n"
        for addr in addrs:
            md += f"- {addr['family']}: {addr['address']}\n"
            if addr['netmask']:
                md += f"  Netmask: {addr['netmask']}\n"
            if addr['broadcast']:
                md += f"  Broadcast: {addr['broadcast']}\n"
    
    md += "\n### Active Connections\n"
    for conn in data['network_info']['connections']:
        md += f"- {conn['type']} {conn['local_addr']} -> {conn['remote_addr']} ({conn['status']})\n"
    
    # Process Information
    md += "\n## Process Information\n"
    md += f"Total Processes: {len(data['process_info'])}\n\n"
    md += "### Top CPU Processes\n"
    top_cpu = sorted(data['process_info'], key=lambda x: x['cpu_percent'], reverse=True)[:10]
    for proc in top_cpu:
        md += f"- {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']}%\n"
    
    md += "\n### Top Memory Processes\n"
    top_memory = sorted(data['process_info'], key=lambda x: x['memory_percent'], reverse=True)[:10]
    for proc in top_memory:
        md += f"- {proc['name']} (PID: {proc['pid']}) - Memory: {proc['memory_percent']}%\n"
    
    # User Information
    md += "\n## User Information\n"
    for user in data['user_info']:
        md += f"- {user['name']} ({user['terminal']}) from {user['host']}\n"
    
    # Security Information
    md += "\n## Security Information\n"
    md += "### Open Ports\n"
    for port in data['security_info']['open_ports']:
        md += f"- {port['protocol']} {port['address']}:{port['port']}\n"
    
    md += "\n### Suspicious Behavior\n"
    if data['suspicious_behavior']['high_cpu_processes']:
        md += "#### High CPU Processes\n"
        for proc in data['suspicious_behavior']['high_cpu_processes']:
            md += f"- {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']}%\n"
    
    if data['suspicious_behavior']['high_memory_processes']:
        md += "\n#### High Memory Processes\n"
        for proc in data['suspicious_behavior']['high_memory_processes']:
            md += f"- {proc['name']} (PID: {proc['pid']}) - Memory: {proc['memory_percent']}%\n"
    
    if data['suspicious_behavior']['unusual_ports']:
        md += "\n#### Unusual Open Ports\n"
        for port in data['suspicious_behavior']['unusual_ports']:
            md += f"- {port['protocol']} {port['address']}:{port['port']}\n"
    
    if data['suspicious_behavior']['suspicious_commands']:
        md += "\n#### Suspicious Commands in History\n"
        for cmd in data['suspicious_behavior']['suspicious_commands']:
            md += f"- `{cmd}`\n"
    
    return md

def generate_html_report(data: Dict[str, Any]) -> str:
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Scan Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2, h3, h4 {{ color: #333; }}
            .section {{ margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .warning {{ color: #ff0000; }}
            .info {{ color: #0000ff; }}
            pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>System Scan Report</h1>
        <p>Generated on: {data['timestamp']}</p>
        
        <div class="section">
            <h2>System Information</h2>
            <table>
                <tr><th>Platform</th><td>{data['system_info']['platform']} {data['system_info']['platform_version']}</td></tr>
                <tr><th>Architecture</th><td>{data['system_info']['architecture']}</td></tr>
                <tr><th>Hostname</th><td>{data['system_info']['hostname']}</td></tr>
                <tr><th>FQDN</th><td>{data['system_info']['fqdn']}</td></tr>
                <tr><th>Python Version</th><td>{data['system_info']['python_version']}</td></tr>
                <tr><th>Boot Time</th><td>{data['system_info']['boot_time']}</td></tr>
                <tr><th>Uptime</th><td>{data['system_info']['system_uptime']:.2f} seconds</td></tr>
                <tr><th>CPU Count</th><td>{data['system_info']['cpu_count']['physical']} physical, {data['system_info']['cpu_count']['logical']} logical</td></tr>
                <tr><th>Memory Usage</th><td>{data['system_info']['memory']['used'] / (1024**3):.2f}GB used ({data['system_info']['memory']['percent']}%)</td></tr>
                <tr><th>Swap Usage</th><td>{data['system_info']['swap']['used'] / (1024**3):.2f}GB used ({data['system_info']['swap']['percent']}%)</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Disk Information</h2>
            <table>
                <tr><th>Device</th><th>Mountpoint</th><th>Filesystem</th><th>Usage</th><th>Free</th></tr>
    """
    
    for disk in data['disk_info']:
        html += f"""
                <tr>
                    <td>{disk['device']}</td>
                    <td>{disk['mountpoint']}</td>
                    <td>{disk['fstype']}</td>
                    <td>{disk['used'] / (1024**3):.2f}GB ({disk['percent']}%)</td>
                    <td>{disk['free'] / (1024**3):.2f}GB</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Network Information</h2>
            <h3>Interfaces</h3>
    """
    
    for interface, addrs in data['network_info']['interfaces'].items():
        html += f"""
            <h4>{interface}</h4>
            <table>
                <tr><th>Family</th><th>Address</th><th>Netmask</th><th>Broadcast</th></tr>
        """
        for addr in addrs:
            html += f"""
                <tr>
                    <td>{addr['family']}</td>
                    <td>{addr['address']}</td>
                    <td>{addr['netmask']}</td>
                    <td>{addr['broadcast']}</td>
                </tr>
            """
        html += """
            </table>
        """
    
    html += """
            <h3>Active Connections</h3>
            <table>
                <tr><th>Type</th><th>Local Address</th><th>Remote Address</th><th>Status</th></tr>
    """
    
    for conn in data['network_info']['connections']:
        html += f"""
                <tr>
                    <td>{conn['type']}</td>
                    <td>{conn['local_addr']}</td>
                    <td>{conn['remote_addr']}</td>
                    <td>{conn['status']}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Process Information</h2>
            <h3>Top CPU Processes</h3>
            <table>
                <tr><th>Name</th><th>PID</th><th>CPU %</th></tr>
    """
    
    top_cpu = sorted(data['process_info'], key=lambda x: x['cpu_percent'], reverse=True)[:10]
    for proc in top_cpu:
        html += f"""
                <tr>
                    <td>{proc['name']}</td>
                    <td>{proc['pid']}</td>
                    <td>{proc['cpu_percent']}%</td>
                </tr>
        """
    
    html += """
            </table>
            
            <h3>Top Memory Processes</h3>
            <table>
                <tr><th>Name</th><th>PID</th><th>Memory %</th></tr>
    """
    
    top_memory = sorted(data['process_info'], key=lambda x: x['memory_percent'], reverse=True)[:10]
    for proc in top_memory:
        html += f"""
                <tr>
                    <td>{proc['name']}</td>
                    <td>{proc['pid']}</td>
                    <td>{proc['memory_percent']}%</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>Security Information</h2>
            <h3>Open Ports</h3>
            <table>
                <tr><th>Protocol</th><th>Address</th><th>Port</th></tr>
    """
    
    for port in data['security_info']['open_ports']:
        html += f"""
                <tr>
                    <td>{port['protocol']}</td>
                    <td>{port['address']}</td>
                    <td>{port['port']}</td>
                </tr>
        """
    
    html += """
            </table>
            
            <h3>Suspicious Behavior</h3>
    """
    
    if data['suspicious_behavior']['high_cpu_processes']:
        html += """
            <h4>High CPU Processes</h4>
            <table>
                <tr><th>Name</th><th>PID</th><th>CPU %</th></tr>
        """
        for proc in data['suspicious_behavior']['high_cpu_processes']:
            html += f"""
                <tr>
                    <td>{proc['name']}</td>
                    <td>{proc['pid']}</td>
                    <td class="warning">{proc['cpu_percent']}%</td>
                </tr>
            """
        html += """
            </table>
        """
    
    if data['suspicious_behavior']['high_memory_processes']:
        html += """
            <h4>High Memory Processes</h4>
            <table>
                <tr><th>Name</th><th>PID</th><th>Memory %</th></tr>
        """
        for proc in data['suspicious_behavior']['high_memory_processes']:
            html += f"""
                <tr>
                    <td>{proc['name']}</td>
                    <td>{proc['pid']}</td>
                    <td class="warning">{proc['memory_percent']}%</td>
                </tr>
            """
        html += """
            </table>
        """
    
    if data['suspicious_behavior']['unusual_ports']:
        html += """
            <h4>Unusual Open Ports</h4>
            <table>
                <tr><th>Protocol</th><th>Address</th><th>Port</th></tr>
        """
        for port in data['suspicious_behavior']['unusual_ports']:
            html += f"""
                <tr>
                    <td>{port['protocol']}</td>
                    <td>{port['address']}</td>
                    <td class="warning">{port['port']}</td>
                </tr>
            """
        html += """
            </table>
        """
    
    if data['suspicious_behavior']['suspicious_commands']:
        html += """
            <h4>Suspicious Commands in History</h4>
            <pre>
        """
        for cmd in data['suspicious_behavior']['suspicious_commands']:
            html += f"{cmd}\n"
        html += """
            </pre>
        """
    
    html += """
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
    report = generate_report(format)
    
    if output:
        with open(output, 'w') as f:
            f.write(report)
        console.print(f"[green]Report saved to {output}[/green]")
    else:
        console.print(report)

if __name__ == '__main__':
    main() 