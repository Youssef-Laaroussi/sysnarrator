import time
import pytest
from sysnarrator.metric_store import MetricStore, MetricSnapshot

def test_metric_store_ring_buffer():
    store = MetricStore(max_samples=5)
    for i in range(10):
        snap = MetricSnapshot(
            timestamp=time.time() + i,
            cpu_percent=10.0 + i,
            cpu_cores=[10.0 + i],
            ram_percent=40.0,
            ram_used_bytes=4000,
            ram_total_bytes=10000,
            swap_percent=0.0,
            disk_percent=50.0,
            disk_used_bytes=50000,
            disk_total_bytes=100000,
            net_read_speed=0.0,
            net_write_speed=0.0,
            disk_read_speed=0.0,
            disk_write_speed=0.0
        )
        store.add_snapshot(snap)

    history = store.get_history()
    assert len(history) == 5
    assert store.get_latest().cpu_percent == 19.0

def test_trend_slope_calculation():
    store = MetricStore(max_samples=20)
    base_time = 1000.0
    for i in range(10):
        # 10 MB per second increase = 600 MB per minute
        snap = MetricSnapshot(
            timestamp=base_time + i,
            cpu_percent=20.0,
            cpu_cores=[20.0],
            ram_percent=40.0,
            ram_used_bytes=(100 + i * 10) * 1024 * 1024,
            ram_total_bytes=2000 * 1024 * 1024,
            swap_percent=0.0,
            disk_percent=50.0,
            disk_used_bytes=50000,
            disk_total_bytes=100000,
            net_read_speed=0.0,
            net_write_speed=0.0,
            disk_read_speed=0.0,
            disk_write_speed=0.0
        )
        store.add_snapshot(snap)

    slope = store.calculate_trend_slope('ram', seconds=30)
    assert 590.0 <= slope <= 610.0
