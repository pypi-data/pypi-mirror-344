"""
Core system scanning functionality
"""

import os
import psutil
import platform
from typing import Dict, List, Any
from datetime import datetime

from ..modules.system import SystemModule
from ..modules.security import SecurityModule
from ..modules.performance import PerformanceModule
from ..modules.network import NetworkModule

class SystemScanner:
    """Main system scanner class"""
    
    def __init__(self, modules: List[str]):
        """Initialize the scanner with specified modules"""
        self.modules = {
            "system": SystemModule(),
            "security": SecurityModule(),
            "performance": PerformanceModule(),
            "network": NetworkModule()
        }
        self.active_modules = {m: self.modules[m] for m in modules}
    
    def scan(self) -> Dict[str, Any]:
        """Run the system scan"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self._get_system_info(),
            "scan_results": {}
        }
        
        for name, module in self.active_modules.items():
            try:
                results["scan_results"][name] = module.scan()
            except Exception as e:
                results["scan_results"][name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        return {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available
            },
            "cpu_count": psutil.cpu_count(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        } 