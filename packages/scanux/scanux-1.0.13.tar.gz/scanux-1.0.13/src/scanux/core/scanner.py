"""
Core system scanning functionality
"""

import os
import psutil
import platform
from typing import Dict, List, Any, Tuple
from datetime import datetime
from .utils import format_size

from ..modules.system import SystemModule
from ..modules.security import SecurityModule
from ..modules.performance import PerformanceModule
from ..modules.network import NetworkModule
from ..modules.users import UserModule

def format_size(size_in_bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} PB"

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
                module_result = module.scan()
                if isinstance(module_result, tuple) and len(module_result) == 2:
                    metrics, issues = module_result
                    results["scan_results"][name] = {
                        "status": "error" if "error" in metrics else "warning" if issues else "ok",
                        "metrics": metrics,
                        "issues": issues
                    }
                else:
                    results["scan_results"][name] = {
                        "status": "ok",
                        "metrics": module_result,
                        "issues": []
                    }
            except Exception as e:
                results["scan_results"][name] = {
                    "status": "error",
                    "metrics": {"error": str(e)},
                    "issues": []
                }
        
        return results
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        mem = psutil.virtual_memory()
        return {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "memory": {
                "total": format_size(mem.total),
                "available": format_size(mem.available),
                "used": format_size(mem.used),
                "percent": f"{mem.percent}%"
            },
            "cpu_count": psutil.cpu_count(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        } 