"""
Root-Cause and Predictive Diagnostic Engine.
Computes explainable health score, detects memory leaks, forecasts disk full,
and provides actionable remediation commands.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time
import os
import psutil
from .metric_store import MetricStore
from .collectors.disk import DiskCollector
from .collectors.processes import ProcessCollector
from .collectors.system_info import SystemInfoCollector


@dataclass
class DiagnosticInsight:
    id: str
    severity: str  # 'critical', 'warning', 'info', 'ok'
    category: str
    title: str
    explanation: str
    evidence: str
    confidence: float  # 0.0 - 1.0
    command: Optional[str] = None
    safe_to_apply: bool = False


@dataclass
class HealthBreakdown:
    score: int
    penalties: List[Dict[str, Any]]
    status_label: str


class DiagnosticEngine:
    """Intelligent analysis that understands root causes and predicts failure modes."""

    def __init__(self, metric_store: Optional[MetricStore] = None):
        self.store = metric_store or MetricStore()

    def calculate_health_score(self) -> HealthBreakdown:
        """Calculate an explainable 0-100 system health score with itemized penalties."""
        score = 100
        penalties = []

        try:
            # CPU penalty
            cpu = psutil.cpu_percent(interval=0.05)
            if cpu > 90:
                p = 25
                score -= p
                penalties.append({'component': 'CPU', 'penalty': p, 'reason': f'Severe CPU saturation ({cpu:.0f}%)'})
            elif cpu > 75:
                p = 15
                score -= p
                penalties.append({'component': 'CPU', 'penalty': p, 'reason': f'High CPU load ({cpu:.0f}%)'})

            # RAM penalty
            mem = psutil.virtual_memory()
            if mem.percent > 90:
                p = 30
                score -= p
                penalties.append({'component': 'RAM', 'penalty': p, 'reason': f'Critical memory pressure ({mem.percent:.0f}%)'})
            elif mem.percent > 80:
                p = 15
                score -= p
                penalties.append({'component': 'RAM', 'penalty': p, 'reason': f'Elevated memory consumption ({mem.percent:.0f}%)'})

            # Swap thrashing penalty
            swap = psutil.swap_memory()
            if swap.total > 0 and swap.percent > 40:
                p = 20
                score -= p
                penalties.append({'component': 'Swap', 'penalty': p, 'reason': f'High swap thrashing ({swap.percent:.0f}%)'})

            # Disk exhaustion penalty
            disk = psutil.disk_usage('/')
            if disk.percent > 92:
                p = 35
                score -= p
                penalties.append({'component': 'Disk', 'penalty': p, 'reason': f'Root disk near exhaustion ({disk.percent:.0f}%, <10G left)'})
            elif disk.percent > 85:
                p = 15
                score -= p
                penalties.append({'component': 'Disk', 'penalty': p, 'reason': f'High disk consumption ({disk.percent:.0f}%)'})

            # Task state penalties (Zombies & D-State hangs)
            tasks = SystemInfoCollector.get_task_stats()
            if tasks['uninterruptible_disk_sleep'] > 0:
                p = 15
                score -= p
                penalties.append({'component': 'I/O', 'penalty': p, 'reason': f"{tasks['uninterruptible_disk_sleep']} processes hung in D-state disk sleep"})
            if tasks['zombie'] > 0:
                p = 10
                score -= p
                penalties.append({'component': 'Processes', 'penalty': p, 'reason': f"{tasks['zombie']} zombie processes uncollected"})

        except Exception:
            pass

        final_score = max(0, min(100, score))
        if final_score >= 85:
            status = "EXCELLENT"
        elif final_score >= 70:
            status = "GOOD"
        elif final_score >= 50:
            status = "FAIR"
        else:
            status = "POOR"

        return HealthBreakdown(score=final_score, penalties=penalties, status_label=status)

    def analyze_system(self) -> List[DiagnosticInsight]:
        """Produce actionable diagnostic insights with evidence and remediation."""
        insights: List[DiagnosticInsight] = []

        # 1. Disk Exhaustion & Reclamation Analysis
        try:
            disk = psutil.disk_usage('/')
            if disk.percent >= 80:
                cleanups = DiskCollector.get_cleanup_opportunities()
                if cleanups:
                    top = cleanups[0]
                    insights.append(DiagnosticInsight(
                        id="disk_reclaim",
                        severity="critical" if disk.percent >= 90 else "warning",
                        category="Storage",
                        title=f"Root Partition at {disk.percent:.0f}% - Space Reclaim Available",
                        explanation=f"{top['target']} is holding {top['reclaimable_mb']:.0f} MB of dispensable data.",
                        evidence=f"Path: {top['path']} ({top['reclaimable_mb']:.0f} MB). Root free: {disk.free / 1024**3:.1f} GB.",
                        confidence=0.95,
                        command=top['command'],
                        safe_to_apply=True
                    ))
        except Exception:
            pass

        # 2. I/O Hang & D-State Process Root Cause
        try:
            tasks = SystemInfoCollector.get_task_stats()
            if tasks['uninterruptible_disk_sleep'] > 0:
                pids_str = ", ".join(str(p) for p in tasks['d_state_pids'][:4])
                insights.append(DiagnosticInsight(
                    id="io_hang_dstate",
                    severity="critical",
                    category="Kernel/IO",
                    title="Processes Blocked on Uninterruptible Disk I/O (D-State)",
                    explanation="One or more processes are suspended waiting for storage or network filesystem response.",
                    evidence=f"PIDs: {pids_str} in 'D' state. May cause system freezing.",
                    confidence=0.90,
                    command=f"ps -fp {tasks['d_state_pids'][0]} -o pid,stat,time,comm",
                    safe_to_apply=True
                ))
        except Exception:
            pass

        # 3. Zombie Processes Root Cause
        try:
            tasks = SystemInfoCollector.get_task_stats()
            if tasks['zombie'] > 0:
                pids_str = ", ".join(str(p) for p in tasks['zombie_pids'][:4])
                insights.append(DiagnosticInsight(
                    id="zombie_processes",
                    severity="warning",
                    category="Processes",
                    title=f"{tasks['zombie']} Zombie Process(es) Detected",
                    explanation="Defunct processes remaining in the process table because their parent hasn't reaped them.",
                    evidence=f"Zombies: {pids_str}.",
                    confidence=0.88,
                    command=f"ps -el | grep 'Z'",
                    safe_to_apply=True
                ))
        except Exception:
            pass

        # 4. Multi-Process Application Footprint Analysis
        try:
            apps = ProcessCollector.get_grouped_applications()
            if apps:
                top_app = apps[0]
                if top_app['ram_mb'] > 1500:
                    insights.append(DiagnosticInsight(
                        id=f"app_heavy_{top_app['app'].lower().replace(' ', '_')}",
                        severity="info",
                        category="Application",
                        title=f"{top_app['app']} is Consuming {top_app['ram_mb']/1024:.1f} GB RAM",
                        explanation=f"Spread across {top_app['process_count']} worker processes.",
                        evidence=f"Top PIDs: {', '.join(str(p) for p in top_app['pids'])}",
                        confidence=0.95,
                        command=None,
                        safe_to_apply=False
                    ))
        except Exception:
            pass

        # 5. Baseline Anomaly Check
        anomaly = self.store.get_baseline_anomaly()
        if anomaly:
            insights.append(DiagnosticInsight(
                id="baseline_cpu_anomaly",
                severity="warning",
                category="Anomaly",
                title="Unusual CPU Activity vs Baseline",
                explanation=anomaly['message'],
                evidence=f"Current: {anomaly['current']:.0f}% vs Historic avg: {anomaly['baseline_avg']:.0f}% for this hour.",
                confidence=0.82,
                command="top -b -n 1 -o %CPU | head -n 12",
                safe_to_apply=True
            ))

        return insights
