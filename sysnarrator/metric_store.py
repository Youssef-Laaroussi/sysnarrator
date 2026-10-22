"""
Thread-safe Metric Store with ring buffers for real-time history and trend analysis.
Stores 10 minutes of samples at 1-second intervals (600 points) and downsamples for baseline.
"""

from dataclasses import dataclass, field
import threading
import time
from collections import deque
from typing import Dict, List, Optional, Any


@dataclass
class MetricSnapshot:
    timestamp: float
    cpu_percent: float
    cpu_cores: List[float]
    ram_percent: float
    ram_used_bytes: int
    ram_total_bytes: int
    swap_percent: float
    disk_percent: float
    disk_used_bytes: int
    disk_total_bytes: int
    net_read_speed: float
    net_write_speed: float
    disk_read_speed: float
    disk_write_speed: float
    temperature_celsius: Optional[float] = None
    tasks_count: int = 0
    threads_count: int = 0
    zombies_count: int = 0
    d_state_count: int = 0


class MetricStore:
    """Thread-safe historical metric repository."""

    def __init__(self, max_samples: int = 600):
        self._max_samples = max_samples
        self._samples: deque[MetricSnapshot] = deque(maxlen=max_samples)
        self._lock = threading.Lock()
        self._hourly_baseline: Dict[int, List[float]] = {h: [] for h in range(24)}

    def add_snapshot(self, snapshot: MetricSnapshot) -> None:
        """Add a snapshot in a thread-safe manner."""
        with self._lock:
            self._samples.append(snapshot)
            # Record CPU in hourly baseline
            tm = time.localtime(snapshot.timestamp)
            hour = tm.tm_hour
            b_list = self._hourly_baseline[hour]
            b_list.append(snapshot.cpu_percent)
            if len(b_list) > 120:
                self._hourly_baseline[hour] = b_list[-120:]

    def populate_demo_data(self, count: int = 60) -> None:
        """Pre-populate with realistic synthetic metrics (sine waves, noise, spikes, leak trend)."""
        import math
        import random
        base_time = time.time() - count
        base_ram = 8 * 1024 * 1024 * 1024
        for i in range(count):
            t = base_time + i
            # Sine wave with noise for CPU
            cpu = 35.0 + 25.0 * math.sin(i / 10.0) + random.uniform(-4.0, 6.0)
            if i in [15, 38, 52]:  # Periodic spikes
                cpu = min(98.0, cpu + 35.0)
            cpu = max(5.0, min(100.0, cpu))

            # Multi-core distribution
            cores = [
                max(2.0, min(100.0, cpu + random.uniform(-10.0, 15.0)))
                for _ in range(4)
            ]

            # Simulated memory leak (+ 15MB each second)
            ram_used = int(base_ram + (i * 15 * 1024 * 1024) + random.randint(-5, 10) * 1024 * 1024)
            total_ram = 16 * 1024 * 1024 * 1024
            ram_pct = (ram_used / total_ram) * 100.0

            # Net and disk throughput
            net_in = max(10.0, 1200.0 + 800.0 * math.sin(i / 7.0) + random.uniform(-150, 150)) # KB/s
            net_out = max(5.0, 350.0 + 150.0 * math.cos(i / 6.0))
            d_read = max(0.0, 2.5 * math.sin(i / 5.0) if i % 10 < 4 else 0.1) # MB/s
            d_write = max(0.1, 8.0 if i in [22, 45] else 0.5)

            snap = MetricSnapshot(
                timestamp=t,
                cpu_percent=cpu,
                cpu_cores=cores,
                ram_percent=ram_pct,
                ram_used_bytes=ram_used,
                ram_total_bytes=total_ram,
                swap_percent=12.5,
                disk_percent=88.5,
                disk_used_bytes=206 * 1024 * 1024 * 1024,
                disk_total_bytes=233 * 1024 * 1024 * 1024,
                net_read_speed=net_in,
                net_write_speed=net_out,
                disk_read_speed=d_read,
                disk_write_speed=d_write,
                temperature_celsius=58.0 + 8.0 * math.sin(i / 12.0),
                tasks_count=342,
                threads_count=1460,
                zombies_count=1 if i > 30 else 0,
                d_state_count=1 if i in range(20, 26) else 0,
            )
            self.add_snapshot(snap)

    def get_latest(self) -> Optional[MetricSnapshot]:
        """Return the most recent snapshot."""
        with self._lock:
            if not self._samples:
                return None
            return self._samples[-1]

    def get_history(self, count: Optional[int] = None) -> List[MetricSnapshot]:
        """Return a slice or full list of historical snapshots."""
        with self._lock:
            if count is None or count >= len(self._samples):
                return list(self._samples)
            return list(self._samples)[-count:]

    def calculate_trend_slope(self, metric_name: str, seconds: int = 60) -> float:
        """
        Calculate trend slope (rate of change per minute) using linear regression
        over the specified time window.
        """
        with self._lock:
            if len(self._samples) < 2:
                return 0.0

            now = self._samples[-1].timestamp
            cutoff = now - seconds
            pts = [s for s in self._samples if s.timestamp >= cutoff]

            if len(pts) < 2:
                return 0.0

            times = [s.timestamp - pts[0].timestamp for s in pts]
            if metric_name == 'cpu':
                vals = [s.cpu_percent for s in pts]
            elif metric_name == 'ram':
                vals = [s.ram_used_bytes / (1024 * 1024) for s in pts]  # MB
            elif metric_name == 'disk':
                vals = [s.disk_used_bytes / (1024 * 1024) for s in pts]  # MB
            else:
                return 0.0

            n = len(times)
            mean_x = sum(times) / n
            mean_y = sum(vals) / n
            num = sum((times[i] - mean_x) * (vals[i] - mean_y) for i in range(n))
            den = sum((times[i] - mean_x) ** 2 for i in range(n))

            if den == 0:
                return 0.0

            slope_per_second = num / den
            return slope_per_second * 60.0  # rate per minute

    def get_baseline_anomaly(self) -> Optional[Dict[str, Any]]:
        """Check if current CPU is an anomaly compared to the machine's hourly baseline."""
        with self._lock:
            if not self._samples:
                return None
            latest = self._samples[-1]
            hour = time.localtime(latest.timestamp).tm_hour
            history_at_hour = self._hourly_baseline.get(hour, [])
            if len(history_at_hour) < 10:
                return None

            avg = sum(history_at_hour) / len(history_at_hour)
            diff = latest.cpu_percent - avg
            if diff > 35.0:
                return {
                    'hour': hour,
                    'current': latest.cpu_percent,
                    'baseline_avg': avg,
                    'severity': 'high',
                    'message': f"CPU is {diff:.0f}% higher than baseline for hour {hour:02d}:00"
                }
            return None
