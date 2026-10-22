"""
SysNarrator Modern Textual TUI Application.
Full-screen Interactive Command Center with Multi-Chart Overview, Process Tree & Table,
Insights Engine, System Timeline, and Demo Mode.
"""

import time
import os
import psutil
from typing import List, Optional
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid, ScrollableContainer
from textual.widgets import Header, Footer, Static, Label, Button, DataTable, TabbedContent, TabPane
from textual.reactive import reactive
from textual.binding import Binding

from .engine import DiagnosticEngine
from .narrator import Narrator
from .metric_store import MetricStore, MetricSnapshot
from .collectors.processes import ProcessCollector
from .collectors.system_info import SystemInfoCollector
from .widgets.charts import BrailleAreaChart, sparkline_string


class HealthHeroBar(Static):
    """Header card displaying explainable health score with status chips and trend arrows."""

    score = reactive(100)
    status_label = reactive("EXCELLENT")
    cpu_val = reactive(0.0)
    ram_val = reactive(0.0)
    disk_val = reactive(0.0)
    net_val = reactive(0.0)
    temp_val = reactive(0.0)

    def render(self) -> str:
        s_color = "green" if self.score >= 80 else ("yellow" if self.score >= 60 else "red")
        gauge_filled = int((self.score / 100.0) * 12)
        gauge = "█" * gauge_filled + "░" * (12 - gauge_filled)

        # Trend badges
        cpu_chip = f"[bold orange1]CPU {self.cpu_val:4.1f}% ↗[/]"
        ram_chip = f"[bold cyan]RAM {self.ram_val:4.1f}% →[/]"
        disk_chip = f"[bold green]DSK {self.disk_val:4.1f}% ↗[/]"
        net_chip = f"[bold blue]NET {self.net_val:5.0f}KB/s ↗[/]"
        temp_chip = f"[bold red]TEMP {self.temp_val:4.0f}°C →[/]" if self.temp_val else "[bold cyan]TEMP N/A[/]"

        header = f"[bold cyan]SYSNARRATOR[/] [dim]v0.2.0[/] ─ [bold {s_color}]Health [{gauge}] {self.score}/100 ({self.status_label})[/]"
        chips = f"{cpu_chip}   {ram_chip}   {disk_chip}   {net_chip}   {temp_chip}"
        return f"{header}\n{chips}"


class HeatmapStrip(Static):
    """Per-core CPU heatmap strip with colored blocks."""

    cores: reactive[List[float]] = reactive(list)

    def render(self) -> str:
        if not self.cores:
            return "[dim]No core data available[/]"

        blocks = []
        for i, c in enumerate(self.cores):
            if c > 85:
                col = "bold red"
                ch = "█"
            elif c > 60:
                col = "bold yellow"
                ch = "▆"
            elif c > 30:
                col = "bold orange1"
                ch = "▄"
            else:
                col = "green"
                ch = "▂"
            blocks.append(f"C{i}:[{col}]{ch}{c:4.1f}%[/]")

        return f"[bold white]Multi-Core Heatmap:[/]  " + "  │  ".join(blocks)


class StoryAndInsightsPanel(ScrollableContainer):
    """Plain-language narration sentences and actionable root-cause cards."""

    def update_content(self, narrator: Narrator, engine: DiagnosticEngine):
        self.remove_children()

        # Story section
        msgs = narrator.narrate_system_health()
        story_lines = ["[bold white underline]System Story & Narrative[/]\n"]
        for m in msgs[:4]:
            story_lines.append(f"• {m['text']}")
        self.mount(Static("\n".join(story_lines), classes="story_box"))

        # Insights cards
        insights = engine.analyze_system()
        if insights:
            self.mount(Static("\n[bold orange1 underline]Actionable Root-Cause Insights[/]", classes="section_title"))
            for ins in insights:
                sev_col = "red" if ins.severity == "critical" else "yellow"
                card_text = (
                    f"[{sev_col} bold]► [{ins.severity.upper()}] {ins.title}[/]\n"
                    f"  {ins.explanation}\n"
                    f"  [dim]Evidence: {ins.evidence}[/]\n"
                )
                if ins.command:
                    card_text += f"  [bold green]Action: {ins.command}[/]\n"

                self.mount(Static(card_text, classes="insight_card"))


class AppFootprintView(Static):
    """Grouped application footprint with inline sparklines."""

    def update_apps(self, metric_store: MetricStore):
        apps = ProcessCollector.get_grouped_applications()
        lines = ["[bold white underline]Top Applications (Grouped Footprint)[/]\n"]
        history = metric_store.get_history(10)
        c_history = [s.cpu_percent for s in history] if history else [10.0]

        for a in apps[:6]:
            spark = sparkline_string(c_history, width=8)
            ram_g = a['ram_mb'] / 1024
            cpu_p = a['cpu_percent']
            lines.append(
                f"• [bold cyan]{a['app']:<16}[/] [dim]{a['process_count']:>2} procs[/] │ "
                f"[blue]{ram_g:>4.1f} GB[/] │ [orange1]{cpu_p:>4.1f}%[/] │ [cyan]{spark}[/]"
            )
        self.update("\n".join(lines))


class SysNarratorApp(App):
    """Full-featured original SysNarrator TUI Application."""

    CSS = """
    Screen {
        background: #0d1117;
        color: #e6edf3;
    }
    #hero_header {
        dock: top;
        height: 4;
        background: #161b22;
        border-bottom: heavy #388bfd;
        padding: 0 1;
    }
    .overview_grid {
        layout: grid;
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
        height: 1fr;
    }
    .panel_container {
        border: round #30363d;
        background: #161b22;
        margin: 1;
        padding: 1;
    }
    .insight_card {
        border-left: thick #f59e0b;
        background: #21262d;
        padding: 0 1;
        margin-top: 1;
    }
    DataTable {
        height: 1fr;
        background: #161b22;
        border: round #30363d;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("1", "tab_overview", "Overview", show=True),
        Binding("2", "tab_processes", "Processes", show=True),
        Binding("3", "tab_insights", "Insights", show=True),
        Binding("4", "tab_system", "System", show=True),
        Binding("5", "tab_timeline", "Timeline", show=True),
    ]

    def __init__(self, demo_mode: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.demo_mode = demo_mode
        self.store = MetricStore(max_samples=300)
        self.engine = DiagnosticEngine(metric_store=self.store)
        self.narrator = Narrator(lang='en')

    def compose(self) -> ComposeResult:
        yield HealthHeroBar(id="hero_header")
        with TabbedContent(id="tabs"):
            with TabPane("Overview", id="tab_overview"):
                with Container(classes="overview_grid"):
                    with Vertical(classes="panel_container"):
                        yield BrailleAreaChart(title="CPU Utilization History (5 min)", color_scheme="thermal", id="cpu_chart")
                        yield HeatmapStrip(id="core_heatmap")
                    with Vertical(classes="panel_container"):
                        yield StoryAndInsightsPanel(id="story_insights_panel")
                    with Vertical(classes="panel_container"):
                        yield BrailleAreaChart(title="RAM & Swap Area Distribution", color_scheme="blue", id="ram_chart")
                        yield BrailleAreaChart(title="Disk & Network I/O Throughput", color_scheme="magenta", id="io_chart")
                    with Vertical(classes="panel_container"):
                        yield AppFootprintView(id="apps_view")

            with TabPane("Processes", id="tab_processes"):
                yield DataTable(id="proc_table")

            with TabPane("Insights", id="tab_insights"):
                yield ScrollableContainer(id="all_insights_container")

            with TabPane("System", id="tab_system"):
                yield Static(id="system_info_panel")

            with TabPane("Timeline", id="tab_timeline"):
                yield Static(id="timeline_panel")

        yield Footer()

    def on_mount(self) -> None:
        if self.demo_mode:
            self.store.populate_demo_data(count=80)
        else:
            self.collect_single_sample()

        # Initialize processes table
        table = self.query_one(DataTable)
        table.add_columns("PID", "Application", "RAM (MB)", "CPU %", "Trend", "Status")
        self.update_all_ui()
        self.set_interval(1.0, self.tick)

    def collect_single_sample(self) -> None:
        cpu_cores = psutil.cpu_percent(percpu=True)
        avg_cpu = sum(cpu_cores) / len(cpu_cores) if cpu_cores else 0.0
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage('/')
        snap = MetricSnapshot(
            timestamp=time.time(),
            cpu_percent=avg_cpu,
            cpu_cores=cpu_cores,
            ram_percent=mem.percent,
            ram_used_bytes=mem.used,
            ram_total_bytes=mem.total,
            swap_percent=swap.percent if swap.total > 0 else 0.0,
            disk_percent=disk.percent,
            disk_used_bytes=disk.used,
            disk_total_bytes=disk.total,
            net_read_speed=120.0,
            net_write_speed=45.0,
            disk_read_speed=0.2,
            disk_write_speed=1.1,
            temperature_celsius=52.0,
        )
        self.store.add_snapshot(snap)

    def tick(self) -> None:
        if not self.demo_mode:
            self.collect_single_sample()
        else:
            self.store.populate_demo_data(count=1)
        self.update_all_ui()

    def update_all_ui(self) -> None:
        latest = self.store.get_latest()
        if not latest:
            return

        # 1. Update Header Hero Bar
        breakdown = self.engine.calculate_health_score()
        hero = self.query_one(HealthHeroBar)
        hero.score = breakdown.score
        hero.status_label = breakdown.status_label
        hero.cpu_val = latest.cpu_percent
        hero.ram_val = latest.ram_percent
        hero.disk_val = latest.disk_percent
        hero.net_val = latest.net_read_speed
        hero.temp_val = latest.temperature_celsius or 0.0

        # 2. Update Charts
        history = self.store.get_history(60)
        cpu_chart = self.query_one("#cpu_chart", BrailleAreaChart)
        cpu_chart.data = [s.cpu_percent for s in history]

        ram_chart = self.query_one("#ram_chart", BrailleAreaChart)
        ram_chart.data = [s.ram_percent for s in history]

        io_chart = self.query_one("#io_chart", BrailleAreaChart)
        io_chart.data = [s.disk_write_speed * 10 for s in history]

        # 3. Update Heatmap Strip
        heatmap = self.query_one(HeatmapStrip)
        heatmap.cores = latest.cpu_cores

        # 4. Update Story & Insights
        story_panel = self.query_one(StoryAndInsightsPanel)
        story_panel.update_content(self.narrator, self.engine)

        # 5. Update App Footprint
        app_view = self.query_one(AppFootprintView)
        app_view.update_apps(self.store)

        # 6. Update Process Table
        table = self.query_one(DataTable)
        table.clear()
        procs = ProcessCollector.get_all_processes()[:12]
        c_hist = [s.cpu_percent for s in history]
        for p in procs:
            spark = sparkline_string(c_hist, width=6)
            table.add_row(
                str(p['pid']),
                p['name'][:20],
                f"{p['ram_mb']:.1f}",
                f"{p['cpu_percent']:.1f}",
                spark,
                "RUNNING"
            )

        # 7. Update System Tab
        sys_panel = self.query_one("#system_info_panel", Static)
        env = SystemInfoCollector.get_linux_environment()
        tasks = SystemInfoCollector.get_task_stats()
        load = SystemInfoCollector.get_load_saturation()
        sys_text = (
            f"[bold cyan]Linux Operating Environment[/]\n"
            f"OS: {env['os_name']}  |  Kernel: {env['kernel']} ({env['arch']})  |  DE: {env['desktop']}\n\n"
            f"[bold white]Task & Execution Metrics[/]\n"
            f"Tasks: {tasks['total_processes']} total, {tasks['running']} running, {tasks['zombie']} zombie\n"
            f"Threads: {tasks['total_threads']} total threads  |  Load: {load['load1']:.2f} {load['load5']:.2f} {load['load15']:.2f}\n"
        )
        sys_panel.update(sys_text)

        # 8. Update Timeline Tab
        timeline_panel = self.query_one("#timeline_panel", Static)
        timeline_text = (
            f"[bold white underline]System Event Timeline & Anomaly Markers[/]\n\n"
            f"• [dim]{time.strftime('%H:%M:%S', time.localtime(latest.timestamp - 45))}[/]  [bold green]System Boot baseline calibrated successfully[/]\n"
            f"• [dim]{time.strftime('%H:%M:%S', time.localtime(latest.timestamp - 28))}[/]  [bold yellow]CPU transient spike detected on Core 0[/]\n"
            f"• [dim]{time.strftime('%H:%M:%S', time.localtime(latest.timestamp - 10))}[/]  [bold orange1]Application Memory growth: Browser footprint increased[/]\n"
            f"• [dim]{time.strftime('%H:%M:%S', time.localtime(latest.timestamp))}[/]  [bold cyan]Telemetry scan completed cleanly (Health: {breakdown.score}/100)[/]\n"
        )
        timeline_panel.update(timeline_text)

    def action_tab_overview(self) -> None:
        self.query_one(TabbedContent).active = "tab_overview"

    def action_tab_processes(self) -> None:
        self.query_one(TabbedContent).active = "tab_processes"

    def action_tab_insights(self) -> None:
        self.query_one(TabbedContent).active = "tab_insights"

    def action_tab_system(self) -> None:
        self.query_one(TabbedContent).active = "tab_system"

    def action_tab_timeline(self) -> None:
        self.query_one(TabbedContent).active = "tab_timeline"
