"""Network Metrics Collector"""
import psutil


class NetworkCollector:
    """Collects network I/O and connection metrics"""

    @staticmethod
    def get_io_counters():
        """Get network I/O statistics"""
        return psutil.net_io_counters()

    @staticmethod
    def get_io_counters_per_nic():
        """Get network I/O statistics per network interface"""
        return psutil.net_io_counters(pernic=True)

    @staticmethod
    def get_connections():
        """Get active network connections"""
        try:
            return psutil.net_connections()
        except (PermissionError, OSError):
            return []

    @staticmethod
    def get_if_addrs():
        """Get network interface addresses"""
        return psutil.net_if_addrs()

    @staticmethod
    def get_if_stats():
        """Get network interface statistics"""
        return psutil.net_if_stats()
