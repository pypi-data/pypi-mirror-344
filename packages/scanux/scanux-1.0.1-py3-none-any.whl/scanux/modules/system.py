"""
System module for basic system checks and metrics
"""

import os
import psutil
import platform
from typing import Dict, Any, List, Tuple
from datetime import datetime

class SystemModule:
    """Handles basic system checks and metrics"""
    
    def __init__(self):
        """Initialize system module"""
        self.metrics = {}
        self.issues = []
    
    def scan(self) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
        """Run system checks and return metrics and issues"""
        try:
            self._check_disk_usage()
            self._check_memory_usage()
            self._check_cpu_usage()
            self._check_system_load()
            self._check_uptime()
            self._check_swap_usage()
            
            return self.metrics, self.issues
            
        except Exception as e:
            return {"error": str(e)}, []
    
    def _check_disk_usage(self):
        """Check disk space usage"""
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.metrics[f"disk_usage_{partition.mountpoint}"] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
                
                if usage.percent > 90:
                    self.issues.append({
                        "severity": "high",
                        "message": f"Disk usage critical on {partition.mountpoint}: {usage.percent}%"
                    })
                elif usage.percent > 80:
                    self.issues.append({
                        "severity": "medium",
                        "message": f"Disk usage high on {partition.mountpoint}: {usage.percent}%"
                    })
            except PermissionError:
                continue
    
    def _check_memory_usage(self):
        """Check memory usage"""
        memory = psutil.virtual_memory()
        self.metrics["memory"] = {
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
            "percent": memory.percent
        }
        
        if memory.percent > 90:
            self.issues.append({
                "severity": "high",
                "message": f"Memory usage critical: {memory.percent}%"
            })
        elif memory.percent > 80:
            self.issues.append({
                "severity": "medium",
                "message": f"Memory usage high: {memory.percent}%"
            })
    
    def _check_cpu_usage(self):
        """Check CPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics["cpu"] = {
            "percent": cpu_percent,
            "count": psutil.cpu_count(),
            "count_logical": psutil.cpu_count(logical=True)
        }
        
        if cpu_percent > 90:
            self.issues.append({
                "severity": "high",
                "message": f"CPU usage critical: {cpu_percent}%"
            })
        elif cpu_percent > 80:
            self.issues.append({
                "severity": "medium",
                "message": f"CPU usage high: {cpu_percent}%"
            })
    
    def _check_system_load(self):
        """Check system load averages"""
        load1, load5, load15 = os.getloadavg()
        cpu_count = psutil.cpu_count()
        
        self.metrics["load_average"] = {
            "1min": load1,
            "5min": load5,
            "15min": load15
        }
        
        if load5 > cpu_count * 2:
            self.issues.append({
                "severity": "high",
                "message": f"System load critical: {load5} (5min average)"
            })
        elif load5 > cpu_count:
            self.issues.append({
                "severity": "medium",
                "message": f"System load high: {load5} (5min average)"
            })
    
    def _check_uptime(self):
        """Check system uptime"""
        boot_time = psutil.boot_time()
        uptime = datetime.now().timestamp() - boot_time
        
        self.metrics["uptime"] = {
            "seconds": uptime,
            "boot_time": boot_time
        }
    
    def _check_swap_usage(self):
        """Check swap memory usage"""
        swap = psutil.swap_memory()
        self.metrics["swap"] = {
            "total": swap.total,
            "used": swap.used,
            "free": swap.free,
            "percent": swap.percent
        }
        
        if swap.percent > 80:
            self.issues.append({
                "severity": "medium",
                "message": f"High swap usage: {swap.percent}%"
            }) 