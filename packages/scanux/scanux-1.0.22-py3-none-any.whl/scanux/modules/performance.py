"""
Performance monitoring module
"""

import os
import psutil
from typing import Dict, Any
from datetime import datetime

class PerformanceModule:
    """Performance monitor"""
    
    def scan(self) -> Dict[str, Any]:
        """Scan performance metrics"""
        return {
            "cpu": self._get_cpu_info(),
            "memory": self._get_memory_info(),
            "disk": self._get_disk_info(),
            "network": self._get_network_info(),
            "processes": self._get_process_info()
        }
    
    def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information and usage"""
        try:
            return {
                "usage_percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "frequency": {
                    "current": psutil.cpu_freq().current,
                    "min": psutil.cpu_freq().min,
                    "max": psutil.cpu_freq().max
                },
                "load_avg": {
                    "1min": os.getloadavg()[0],
                    "5min": os.getloadavg()[1],
                    "15min": os.getloadavg()[2]
                }
            }
        except:
            return {"error": "Could not get CPU information"}
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information and usage"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            return {
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "percent": memory.percent
                },
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent
                }
            }
        except:
            return {"error": "Could not get memory information"}
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information and usage"""
        try:
            disk_info = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info[partition.mountpoint] = {
                        "device": partition.device,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    }
                except:
                    continue
            return disk_info
        except:
            return {"error": "Could not get disk information"}
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information and usage"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            }
        except:
            return {"error": "Could not get network information"}
    
    def _get_process_info(self) -> Dict[str, Any]:
        """Get process information"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": proc.info['memory_percent']
                    })
                except:
                    continue
            return {"processes": processes}
        except:
            return {"error": "Could not get process information"} 