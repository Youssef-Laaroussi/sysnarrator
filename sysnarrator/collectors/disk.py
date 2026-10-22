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

    @staticmethod
    def get_cleanup_opportunities():
        """Fast scan common reclaimable locations and suggest safe cleanup commands without hanging"""
        import subprocess
        opportunities = []
        home = os.path.expanduser('~')
        targets = [
            ('User Cache (~/.cache)', os.path.join(home, '.cache'), 'rm -rf ~/.cache/*'),
            ('System Journal Logs (/var/log/journal)', '/var/log/journal', 'sudo journalctl --vacuum-size=200M'),
            ('System Log Files (/var/log)', '/var/log', 'sudo truncate -s 0 /var/log/*.log'),
            ('APT Package Cache', '/var/cache/apt/archives', 'sudo apt-get clean'),
            ('User Trash Bin', os.path.join(home, '.local/share/Trash'), 'rm -rf ~/.local/share/Trash/*'),
            ('Temporary Files (/tmp)', '/tmp', 'sudo rm -rf /tmp/*'),
        ]

        for label, path, cmd in targets:
            if not os.path.exists(path):
                continue
            try:
                # du with short 0.5s timeout for instantaneous responsiveness
                res = subprocess.run(['du', '-sBM', path], capture_output=True, text=True, timeout=0.4)
                if res.returncode == 0 and res.stdout:
                    mb_str = res.stdout.split()[0].replace('M', '')
                    mb = float(mb_str)
                    if mb >= 50.0:
                        opportunities.append({
                            'target': label,
                            'path': path,
                            'reclaimable_mb': mb,
                            'reclaimable_gb': mb / 1024,
                            'command': cmd
                        })
            except Exception:
                pass

        opportunities.sort(key=lambda x: x['reclaimable_mb'], reverse=True)
        return opportunities
