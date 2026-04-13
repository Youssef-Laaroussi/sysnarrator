"""CPU Metrics Collector"""
import psutil


class CPUCollector:
    """Collects CPU usage metrics"""

    @staticmethod
    def get_overall_percent(interval=0.5):
        """Get overall CPU usage percentage"""
        return psutil.cpu_percent(interval=interval)

    @staticmethod
    def get_per_core_percent(interval=0.1):
        """Get per-core CPU usage percentages"""
        return psutil.cpu_percent(interval=interval, percpu=True)

    @staticmethod
    def get_frequency():
        """Get CPU frequency information"""
        return psutil.cpu_freq()

    @staticmethod
    def get_count():
        """Get number of CPU cores"""
        return psutil.cpu_count()
