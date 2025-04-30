"""
Network module for network security and performance checks
"""

import socket
import nmap
import netifaces
from typing import Dict, Any, List, Tuple
import subprocess
import re

class NetworkModule:
    """Handles network security and performance checks"""
    
    def __init__(self):
        """Initialize network module"""
        self.metrics = {}
        self.issues = []
        self.nm = nmap.PortScanner()
    
    def scan(self) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
        """Run network checks and return metrics and issues"""
        try:
            self._scan_ports()
            self._get_listening_services()
            self._check_network_connections()
            self._check_firewall()
            self._check_interfaces()
            
            return self.metrics, self.issues
            
        except Exception as e:
            return {"error": str(e)}, []
    
    def _scan_ports(self):
        """Scan for open ports"""
        try:
            # Scan localhost for common ports
            self.nm.scan('127.0.0.1', arguments='-F')
            open_ports = []
            
            if '127.0.0.1' in self.nm.all_hosts():
                for proto in self.nm['127.0.0.1'].all_protocols():
                    ports = self.nm['127.0.0.1'][proto].keys()
                    for port in ports:
                        state = self.nm['127.0.0.1'][proto][port]['state']
                        if state == 'open':
                            open_ports.append({
                                'port': port,
                                'protocol': proto,
                                'service': self.nm['127.0.0.1'][proto][port]['name']
                            })
            
            self.metrics['open_ports'] = open_ports
            
            # Check for potentially dangerous ports
            dangerous_ports = [21, 23, 445, 3389]  # FTP, Telnet, SMB, RDP
            for port_info in open_ports:
                if port_info['port'] in dangerous_ports:
                    self.issues.append({
                        "severity": "high",
                        "message": f"Potentially dangerous port {port_info['port']} ({port_info['service']}) is open"
                    })
                    
        except Exception as e:
            self.issues.append({
                "severity": "medium",
                "message": f"Port scan failed: {str(e)}"
            })
    
    def _get_listening_services(self):
        """Get list of listening services"""
        try:
            output = subprocess.check_output(['netstat', '-tuln']).decode()
            listening = []
            
            for line in output.split('\n'):
                if 'LISTEN' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        addr = parts[3]
                        listening.append(addr)
            
            self.metrics['listening_services'] = listening
            
        except Exception:
            pass
    
    def _check_network_connections(self):
        """Check active network connections"""
        connections = []
        try:
            for conn in socket.socket(socket.AF_INET, socket.SOCK_STREAM).getsockname():
                connections.append({
                    'local_address': conn.laddr.ip,
                    'local_port': conn.laddr.port,
                    'remote_address': conn.raddr.ip if conn.raddr else None,
                    'remote_port': conn.raddr.port if conn.raddr else None,
                    'status': conn.status
                })
            
            self.metrics['active_connections'] = connections
            
        except Exception:
            pass
    
    def _check_firewall(self):
        """Check firewall status"""
        try:
            # Try checking UFW status
            output = subprocess.check_output(['ufw', 'status']).decode()
            if 'Status: inactive' in output:
                self.issues.append({
                    "severity": "high",
                    "message": "Firewall (UFW) is inactive"
                })
            self.metrics['firewall'] = {'type': 'ufw', 'active': 'Status: active' in output}
        except Exception:
            try:
                # Try checking iptables
                output = subprocess.check_output(['iptables', '-L']).decode()
                rules = len(output.split('\n'))
                self.metrics['firewall'] = {'type': 'iptables', 'rules': rules}
            except Exception:
                self.metrics['firewall'] = {'type': 'unknown', 'status': 'unknown'}
    
    def _check_interfaces(self):
        """Check network interfaces"""
        interfaces = []
        for iface in netifaces.interfaces():
            try:
                addrs = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        interfaces.append({
                            'name': iface,
                            'ip': addr['addr'],
                            'netmask': addr['netmask']
                        })
            except Exception:
                continue
        
        self.metrics['interfaces'] = interfaces 