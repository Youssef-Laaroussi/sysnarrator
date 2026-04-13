"""Disk Metrics Collector"""
import psutil
import os


class DiskCollector:
    """Collects disk usage and I/O metrics"""

    @staticmethod
    def get_disk_usage(path='/'):
        """Get disk usage statistics for a given path"""
        try:
            return psutil.disk_usage(path)
        except (FileNotFoundError, PermissionError):
            return None

    @staticmethod
    def get_all_partitions():
        """Get all disk partitions"""
        return psutil.disk_partitions()

    @staticmethod
    def get_disk_io_counters():
        """Get disk I/O counters"""
        return psutil.disk_io_counters()

    @staticmethod
    def get_disk_usage_percent(path='/'):
        """Get disk usage percentage for a given path"""
        usage = DiskCollector.get_disk_usage(path)
        if usage:
            return usage.percent
        return None
