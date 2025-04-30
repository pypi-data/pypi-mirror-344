"""
Network scanning module
"""

import nmap
import netifaces
import socket
import subprocess
from typing import Dict, Any, List
from datetime import datetime

class NetworkModule:
    """Network scanner"""
    
    def scan(self) -> Dict[str, Any]:
        """Scan network information"""
        return {
            "interfaces": self._get_network_interfaces(),
            "open_ports": self._scan_ports(),
            "connections": self._get_connections(),
            "firewall": self._check_firewall()
        }
    
    def _get_network_interfaces(self) -> Dict[str, Any]:
        """Get network interfaces information"""
        try:
            interfaces = {}
            for iface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(iface)
                interfaces[iface] = {
                    "mac": addrs.get(netifaces.AF_LINK, [{}])[0].get('addr', ''),
                    "ipv4": [addr['addr'] for addr in addrs.get(netifaces.AF_INET, [])],
                    "ipv6": [addr['addr'] for addr in addrs.get(netifaces.AF_INET6, [])]
                }
            return interfaces
        except:
            return {"error": "Could not get network interfaces"}
    
    def _scan_ports(self) -> Dict[str, Any]:
        """Scan for open ports"""
        try:
            nm = nmap.PortScanner()
            nm.scan('127.0.0.1', '20-443')
            
            open_ports = []
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports = nm[host][proto].keys()
                    for port in ports:
                        state = nm[host][proto][port]['state']
                        if state == 'open':
                            open_ports.append({
                                "port": port,
                                "protocol": proto,
                                "service": nm[host][proto][port].get('name', 'unknown')
                            })
            
            return {"open_ports": open_ports}
        except:
            return {"error": "Could not scan ports"}
    
    def _get_connections(self) -> Dict[str, Any]:
        """Get network connections"""
        try:
            result = subprocess.run(
                ["netstat", "-tuln"],
                capture_output=True,
                text=True
            )
            
            connections = []
            for line in result.stdout.split('\n')[2:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        proto = parts[0]
                        local = parts[3]
                        if ':' in local:
                            port = local.split(':')[-1]
                            connections.append({
                                "protocol": proto,
                                "port": port,
                                "address": local
                            })
            
            return {"connections": connections}
        except:
            return {"error": "Could not get network connections"}
    
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