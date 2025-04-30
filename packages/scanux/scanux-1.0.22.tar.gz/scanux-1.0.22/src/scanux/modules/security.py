"""
Security scanning module
"""

import os
import subprocess
from typing import Dict, Any, List
from datetime import datetime

class SecurityModule:
    """Security scanner"""
    
    def scan(self) -> Dict[str, Any]:
        """Scan security information"""
        return {
            "firewall_status": self._check_firewall(),
            "open_ports": self._scan_ports(),
            "sudo_users": self._get_sudo_users(),
            "ssh_status": self._check_ssh(),
            "last_logins": self._get_last_logins(),
            "failed_logins": self._get_failed_logins()
        }
    
    def _check_firewall(self) -> Dict[str, Any]:
        """Check firewall status"""
        try:
            # Check for common firewalls
            firewalls = {
                "ufw": "ufw status",
                "firewalld": "firewall-cmd --state",
                "iptables": "iptables -L"
            }
            
            status = {}
            for name, cmd in firewalls.items():
                try:
                    result = subprocess.run(cmd.split(), capture_output=True, text=True)
                    status[name] = "active" if result.returncode == 0 else "inactive"
                except:
                    status[name] = "not_installed"
            
            return status
        except:
            return {"error": "Could not check firewall status"}
    
    def _scan_ports(self) -> Dict[str, Any]:
        """Scan for open ports"""
        try:
            # Use netstat to get listening ports
            result = subprocess.run(
                ["netstat", "-tuln"],
                capture_output=True,
                text=True
            )
            
            ports = []
            for line in result.stdout.split('\n')[2:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        proto = parts[0]
                        address = parts[3]
                        if ':' in address:
                            port = address.split(':')[-1]
                            ports.append({
                                "protocol": proto,
                                "port": port,
                                "address": address
                            })
            
            return {"open_ports": ports}
        except:
            return {"error": "Could not scan ports"}
    
    def _get_sudo_users(self) -> List[str]:
        """Get list of users with sudo access"""
        try:
            with open('/etc/group', 'r') as f:
                for line in f:
                    if line.startswith('sudo:'):
                        return line.strip().split(':')[-1].split(',')
            return []
        except:
            return []
    
    def _check_ssh(self) -> Dict[str, Any]:
        """Check SSH service status"""
        try:
            result = subprocess.run(
                ["systemctl", "status", "ssh"],
                capture_output=True,
                text=True
            )
            return {
                "status": "active" if "active (running)" in result.stdout else "inactive",
                "details": result.stdout
            }
        except:
            return {"status": "unknown"}
    
    def _get_last_logins(self) -> List[Dict[str, str]]:
        """Get recent login attempts"""
        try:
            result = subprocess.run(
                ["last", "-n", "10"],
                capture_output=True,
                text=True
            )
            logins = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        logins.append({
                            "user": parts[0],
                            "from": parts[2],
                            "when": ' '.join(parts[3:])
                        })
            return logins
        except:
            return []
    
    def _get_failed_logins(self) -> List[Dict[str, str]]:
        """Get failed login attempts"""
        try:
            result = subprocess.run(
                ["lastb", "-n", "10"],
                capture_output=True,
                text=True
            )
            failed = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        failed.append({
                            "user": parts[0],
                            "from": parts[2],
                            "when": ' '.join(parts[3:])
                        })
            return failed
        except:
            return [] 