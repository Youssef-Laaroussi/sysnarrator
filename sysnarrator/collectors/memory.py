"""Memory Metrics Collector"""
import psutil


class MemoryCollector:
    """Collects memory and swap usage metrics"""

    @staticmethod
    def get_virtual_memory():
        """Get virtual memory (RAM) statistics"""
        return psutil.virtual_memory()

    @staticmethod
    def get_swap_memory():
        """Get swap memory statistics"""
        return psutil.swap_memory()

    @staticmethod
    def get_memory_percent():
        """Get memory usage percentage"""
        return psutil.virtual_memory().percent

    @staticmethod
    def get_available_memory_mb():
        """Get available memory in MB"""
        return psutil.virtual_memory().available / 1024 / 1024
