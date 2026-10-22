"""Unit tests for collectors."""
import pytest
from sysnarrator.collectors.cpu import CPUCollector
from sysnarrator.collectors.memory import MemoryCollector
from sysnarrator.collectors.disk import DiskCollector
from sysnarrator.collectors.network import NetworkCollector
from sysnarrator.collectors.processes import ProcessCollector
from sysnarrator.collectors.system_info import SystemInfoCollector


class TestCollectors:

    def test_cpu_collector(self):
        assert CPUCollector.get_overall_percent(interval=0.1) >= 0.0
        assert len(CPUCollector.get_per_core_percent(interval=0.1)) > 0
        assert CPUCollector.get_count() > 0

    def test_memory_collector(self):
        mem = MemoryCollector.get_virtual_memory()
        assert mem.total > 0
        assert 0.0 <= MemoryCollector.get_memory_percent() <= 100.0
        assert MemoryCollector.get_available_memory_mb() > 0

    def test_disk_collector(self):
        usage = DiskCollector.get_disk_usage('/')
        assert usage is not None
        assert 0.0 <= DiskCollector.get_disk_usage_percent('/') <= 100.0
        assert len(DiskCollector.get_all_partitions()) > 0

    def test_network_collector(self):
        io = NetworkCollector.get_io_counters()
        assert io.bytes_recv >= 0
        assert io.bytes_sent >= 0

    def test_process_collector(self):
        procs = ProcessCollector.get_all_processes()
        assert len(procs) > 0
        top_mem = ProcessCollector.get_top_processes_by_memory(n=3)
        assert len(top_mem) <= 3
        top_cpu = ProcessCollector.get_top_processes_by_cpu(n=3)
        assert len(top_cpu) <= 3

    def test_system_info_collector(self):
        env = SystemInfoCollector.get_linux_environment()
        assert 'os_name' in env
        assert 'kernel' in env
        assert 'arch' in env

        tasks = SystemInfoCollector.get_task_stats()
        assert tasks['total_processes'] > 0
        assert tasks['running'] >= 0
        assert tasks['zombie'] >= 0

        load = SystemInfoCollector.get_load_saturation()
        assert load['cores'] > 0
        assert load['saturation1_pct'] >= 0.0
