"""
System information module
"""

import os
import platform
import subprocess
from typing import Dict, Any
from datetime import datetime

class SystemModule:
    """System information scanner"""
    
    def scan(self) -> Dict[str, Any]:
        """Scan system information"""
        return {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "uptime": self._get_uptime(),
            "kernel": self._get_kernel_info(),
            "timezone": self._get_timezone(),
            "last_boot": datetime.fromtimestamp(self._get_boot_time()).isoformat()
        }
    
    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                return str(datetime.fromtimestamp(uptime_seconds))
        except:
            return "Unknown"
    
    def _get_kernel_info(self) -> Dict[str, str]:
        """Get kernel information"""
        try:
            uname = platform.uname()
            return {
                "system": uname.system,
                "node": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine
            }
        except:
            return {"error": "Could not get kernel info"}
    
    def _get_timezone(self) -> str:
        """Get system timezone"""
        try:
            if os.path.exists('/etc/timezone'):
                with open('/etc/timezone', 'r') as f:
                    return f.read().strip()
            elif os.path.exists('/etc/localtime'):
                return os.readlink('/etc/localtime').split('/')[-1]
            else:
                return "Unknown"
        except:
            return "Unknown"
    
    def _get_boot_time(self) -> float:
        """Get system boot time"""
        try:
            return float(subprocess.check_output(['cat', '/proc/stat']).decode().split('\n')[0].split()[1])
        except:
            return 0.0 