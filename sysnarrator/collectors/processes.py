"""Process Metrics Collector"""
import psutil


class ProcessCollector:
    """Collects process information and metrics"""

    @staticmethod
    def get_all_processes():
        """Get all running processes with their info"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'ram_mb': proc.info['memory_info'].rss / 1024 / 1024,
                    'cpu_percent': proc.info['cpu_percent'],
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return processes

    @staticmethod
    def get_process_info(pid):
        """Get information about a specific process"""
        try:
            proc = psutil.Process(pid)
            return {
                'pid': proc.pid,
                'name': proc.name(),
                'ram_mb': proc.memory_info().rss / 1024 / 1024,
                'cpu_percent': proc.cpu_percent(interval=0.1),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    @staticmethod
    def get_top_processes_by_memory(n=5):
        """Get top N processes by memory usage"""
        processes = ProcessCollector.get_all_processes()
        return sorted(processes, key=lambda x: x['ram_mb'], reverse=True)[:n]

    @staticmethod
    def get_top_processes_by_cpu(n=5):
        """Get top N processes by CPU usage"""
        processes = ProcessCollector.get_all_processes()
        return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:n]

    @staticmethod
    def get_top_processes_by_io(n=5):
        """Get top N processes by disk I/O activity (surpasses iotop/htop)"""
        io_procs = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                io_counters = proc.io_counters()
                total_io_mb = (io_counters.read_bytes + io_counters.write_bytes) / 1024 / 1024
                io_procs.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'read_mb': io_counters.read_bytes / 1024 / 1024,
                    'write_mb': io_counters.write_bytes / 1024 / 1024,
                    'total_io_mb': total_io_mb,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                pass
        return sorted(io_procs, key=lambda x: x['total_io_mb'], reverse=True)[:n]

    @staticmethod
    def get_pids():
        """Get all process IDs"""
        return psutil.pids()

