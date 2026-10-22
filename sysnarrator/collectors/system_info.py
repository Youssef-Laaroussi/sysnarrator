"""
Linux System & Environment Collector
Gathers complete OS background, kernel, distribution, desktop environment,
task accounting, and hardware power states.
"""
import os
import platform
import psutil


class SystemInfoCollector:
    """Collects comprehensive Linux OS environment & hardware background data."""

    @staticmethod
    def get_os_release() -> dict:
        """Get Linux distribution details (Ubuntu, Debian, Fedora, Arch, etc.)."""
        info = {
            'distro': 'Linux',
            'version': '',
            'id': 'linux',
            'pretty_name': 'Linux'
        }
        try:
            if hasattr(platform, 'freedesktop_os_release'):
                data = platform.freedesktop_os_release()
                info['distro'] = data.get('NAME', 'Linux')
                info['version'] = data.get('VERSION_ID', '')
                info['id'] = data.get('ID', 'linux')
                info['pretty_name'] = data.get('PRETTY_NAME', f"{info['distro']} {info['version']}".strip())
                return info
        except Exception:
            pass

        # Fallback reading /etc/os-release manually
        try:
            if os.path.exists('/etc/os-release'):
                with open('/etc/os-release', 'r', encoding='utf-8') as f:
                    for line in f:
                        if '=' in line:
                            k, v = line.strip().split('=', 1)
                            v = v.strip('"\'')
                            if k == 'NAME':
                                info['distro'] = v
                            elif k == 'VERSION_ID':
                                info['version'] = v
                            elif k == 'ID':
                                info['id'] = v
                            elif k == 'PRETTY_NAME':
                                info['pretty_name'] = v
                return info
        except Exception:
            pass

        info['pretty_name'] = platform.system()
        return info

    @staticmethod
    def get_linux_environment() -> dict:
        """Get kernel, architecture, desktop session, and hostname."""
        os_info = SystemInfoCollector.get_os_release()
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', os.environ.get('DESKTOP_SESSION', 'Headless / Terminal'))
        session_type = os.environ.get('XDG_SESSION_TYPE', 'cli')

        return {
            'os_name': os_info['pretty_name'],
            'distro_id': os_info['id'],
            'kernel': platform.release(),
            'arch': platform.machine(),
            'hostname': platform.node(),
            'desktop': desktop,
            'session_type': session_type,
            'cpu_count_logical': psutil.cpu_count(logical=True) or 1,
            'cpu_count_physical': psutil.cpu_count(logical=False) or 1,
        }

    @staticmethod
    def get_task_stats() -> dict:
        """Collect deep task & thread stats (running, sleeping, zombies, D-state)."""
        stats = {
            'total_processes': 0,
            'total_threads': 0,
            'running': 0,
            'sleeping': 0,
            'stopped': 0,
            'zombie': 0,
            'uninterruptible_disk_sleep': 0,  # D state - critical bottleneck cause
            'zombie_pids': [],
            'd_state_pids': [],
        }

        for p in psutil.process_iter(['pid', 'status', 'num_threads']):
            try:
                stats['total_processes'] += 1
                status = p.info.get('status')
                threads = p.info.get('num_threads') or 1
                stats['total_threads'] += threads

                if status == psutil.STATUS_RUNNING:
                    stats['running'] += 1
                elif status == psutil.STATUS_SLEEPING:
                    stats['sleeping'] += 1
                elif status == psutil.STATUS_STOPPED:
                    stats['stopped'] += 1
                elif status == psutil.STATUS_ZOMBIE:
                    stats['zombie'] += 1
                    stats['zombie_pids'].append(p.info['pid'])
                elif status == psutil.STATUS_DISK_SLEEP:
                    stats['uninterruptible_disk_sleep'] += 1
                    stats['d_state_pids'].append(p.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return stats

    @staticmethod
    def get_load_saturation() -> dict:
        """Compute load average and core saturation percentages (1m, 5m, 15m)."""
        cores = psutil.cpu_count(logical=True) or 1
        load1, load5, load15 = (0.0, 0.0, 0.0)
        try:
            load1, load5, load15 = psutil.getloadavg()
        except (AttributeError, OSError):
            pass

        return {
            'load1': load1,
            'load5': load5,
            'load15': load15,
            'saturation1_pct': round((load1 / cores) * 100, 1),
            'saturation5_pct': round((load5 / cores) * 100, 1),
            'saturation15_pct': round((load15 / cores) * 100, 1),
            'cores': cores,
        }

    @staticmethod
    def get_battery_info() -> dict | None:
        """Get laptop battery state, percentage, and remaining runtime."""
        try:
            battery = psutil.sensors_battery()
            if not battery:
                return None
            return {
                'percent': battery.percent,
                'power_plugged': battery.power_plugged,
                'secsleft': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
            }
        except Exception:
            return None
