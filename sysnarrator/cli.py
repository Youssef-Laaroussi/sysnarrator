#!/usr/bin/env python3
"""SysNarrator CLI — Entry point"""

import argparse
import json
import time
import os
import sys
from datetime import datetime
from . import __version__
from .narrator import Narrator
from .collectors.system_info import SystemInfoCollector
import psutil

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    YELLOW  = "\033[93m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    # Professional colors
    ORANGE  = "\033[38;5;208m"
    BLUE    = "\033[38;5;33m"
    GREEN_PRO = "\033[38;5;76m"
    RED_PRO = "\033[38;5;196m"
    YELLOW_PRO = "\033[38;5;226m"

LEVEL_COLORS = {
    'critical': C.RED_PRO,
    'warning':  C.YELLOW_PRO,
    'ok':       C.GREEN_PRO,
    'info':     C.BLUE,
}


CATEGORY_COLORS = {
    'system': C.GREEN_PRO,
    'cpu': C.ORANGE,
    'ram': C.BLUE,
    'disk': C.GREEN_PRO,
    'network': C.BLUE,
    'processes': C.BLUE,
    'temperature': C.ORANGE,
}

ALL_MODULES = ['cpu', 'ram', 'disk', 'network', 'processes', 'temperature', 'uptime', 'system']


def clear_screen():
    os.system('clear')


def _severity_color(percent: float) -> str:
    if percent >= 90:
        return C.RED_PRO
    if percent >= 75:
        return C.YELLOW_PRO
    if percent >= 50:
        return C.ORANGE
    return C.GREEN_PRO


def print_colored_bar(label, percent, width=30, no_color=False, base_color: str | None = None):
    """Print resource meter bar.

    Design rule: bar color is stable per resource (CPU=orange, Mem=blue, Disk=green),
    while the percentage text reflects severity (green/orange/yellow/red).
    """
    percent = max(0.0, min(100.0, float(percent)))
    filled = int(percent / 100 * width)
    empty = width - filled

    bar_color = base_color or C.GREEN_PRO
    pct_color = _severity_color(percent)

    if no_color:
        bar = '█' * filled + '░' * empty
        return f"  {label:8} [{bar}] {percent:5.1f}%"

    bar = f"{bar_color}{C.BOLD}{'█' * filled}{C.RESET}{C.DIM}{'░' * empty}{C.RESET}"
    return f"  {label:8} [{bar}] {pct_color}{C.BOLD}{percent:5.1f}%{C.RESET}"


SPARK_BLOCKS = " ▂▃▄▅▆▇█"

def make_sparkline(values, width=12):
    """Generate high-density block sparkline graph."""
    if not values:
        return " " * width
    v = list(values)[-width:]
    if len(v) < width:
        v = [v[0]] * (width - len(v)) + v
    mn, mx = 0.0, 100.0
    res = []
    for x in v:
        idx = int(min(7, max(0, ((x - mn) / (mx - mn or 1)) * 7)))
        res.append(SPARK_BLOCKS[idx])
    return "".join(res)


def print_colored_meter(label, percent, width=18, no_color=False, base_color=None):
    """Render a sleek high-contrast meter bar."""
    percent = max(0.0, min(100.0, float(percent)))
    filled = int(percent / 100 * width)
    empty = width - filled
    bar_color = base_color or C.GREEN_PRO
    pct_color = _severity_color(percent)

    if no_color:
        return f"{label:7} [{'|' * filled}{'.' * empty}] {percent:4.1f}%"
    return f"{C.DIM}{label:7}{C.RESET} [{bar_color}{C.BOLD}{'■' * filled}{C.RESET}{C.DIM}{'·' * empty}{C.RESET}] {pct_color}{percent:4.1f}%{C.RESET}"


def print_dashboard_view(no_color=False):
    """Print high-density multi-panel dashboard cards."""
    width = 78
    now = datetime.now().strftime("%H:%M:%S")
    hostname = os.uname().nodename
    version = f"v{__version__}"

    # Telemetry
    cpu_cores = psutil.cpu_percent(interval=0.1, percpu=True)
    avg_cpu = sum(cpu_cores) / len(cpu_cores) if cpu_cores else 0.0
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')

    try:
        env = SystemInfoCollector.get_linux_environment()
        tasks = SystemInfoCollector.get_task_stats()
        load = SystemInfoCollector.get_load_saturation()
        os_badge = f"{env['os_name']}  |  Linux {env['kernel']} ({env['arch']})"
        task_badge = f"Tasks: {tasks['total_processes']} total, {tasks['running']} running, {tasks['zombie']} zombie"
        load_badge = f"Load: {load['load1']:.2f} {load['load5']:.2f} {load['load15']:.2f} ({load['saturation1_pct']:.0f}% cap on {len(cpu_cores)} cores)"
    except Exception:
        os_badge = "Linux Performance Intelligence"
        task_badge = ""
        load_badge = ""

    # Top Brand Header Card
    if no_color:
        print(f"+{'-'*(width-2)}+")
        print(f"|  SYSNARRATOR {version}  |  {now}  |  Host: {hostname}")
        print(f"|  {os_badge}")
        if task_badge:
            print(f"|  {task_badge}  |  {load_badge}")
        print(f"+{'-'*(width-2)}+")
    else:
        print(f"{C.CYAN}┌{'─'*(width-2)}┐{C.RESET}")
        print(f"{C.CYAN}│{C.RESET}  {C.BOLD}{C.WHITE}SYSNARRATOR{C.RESET} {C.DIM}{version}{C.RESET}  {C.CYAN}│{C.RESET}  {C.CYAN}{now}{C.RESET}  {C.CYAN}│{C.RESET}  Host: {C.MAGENTA}{hostname}{C.RESET}")
        print(f"{C.CYAN}│{C.RESET}  {C.DIM}{os_badge}{C.RESET}")
        if task_badge:
            print(f"{C.CYAN}│{C.RESET}  {C.DIM}{task_badge}  │  {load_badge}{C.RESET}")
        print(f"{C.CYAN}└{'─'*(width-2)}┘{C.RESET}")

    # Visual Core Metrics Card
    spark = make_sparkline(cpu_cores, width=len(cpu_cores) * 3)
    if no_color:
        print("\n[PER-CORE CPU & TELEMETRY GAUGES]")
    else:
        print(f"\n{C.BOLD}{C.WHITE}  TELEMETRY GAUGES & MULTI-CORE BREAKDOWN{C.RESET}  {C.CYAN}[{spark}]{C.RESET}")

    # Core lines in 2 columns
    for i in range(0, len(cpu_cores), 2):
        c1 = f"Core {i}"
        m1 = print_colored_meter(c1, cpu_cores[i], width=14, no_color=no_color, base_color=C.ORANGE)
        if i + 1 < len(cpu_cores):
            c2 = f"Core {i+1}"
            m2 = print_colored_meter(c2, cpu_cores[i+1], width=14, no_color=no_color, base_color=C.ORANGE)
            print(f"  {m1}   │   {m2}")
        else:
            print(f"  {m1}")

    # Global gauges
    print()
    m_cpu = print_colored_meter("CPU Total", avg_cpu, width=22, no_color=no_color, base_color=C.ORANGE)
    m_ram = print_colored_meter(f"RAM {mem.used/1024**3:.1f}/{mem.total/1024**3:.0f}G", mem.percent, width=22, no_color=no_color, base_color=C.BLUE)
    print(f"  {m_cpu}   │   {m_ram}")

    m_dsk = print_colored_meter(f"Disk {disk.used/1024**3:.0f}/{disk.total/1024**3:.0f}G", disk.percent, width=22, no_color=no_color, base_color=C.GREEN_PRO)
    swap_pct = swap.percent if swap.total > 0 else 0.0
    m_swp = print_colored_meter(f"Swap {swap.used/1024**3:.1f}/{swap.total/1024**3:.0f}G", swap_pct, width=22, no_color=no_color, base_color=C.BLUE)
    print(f"  {m_dsk}   │   {m_swp}")
    print()


def print_messages(messages, no_color=False):
    last_category = None
    for msg in messages:
        cat = msg.get('category', '')
        text = msg['text']
        level = msg.get('level', 'info')

        if cat and cat != last_category:
            if no_color:
                print(f"\n  [{cat.upper()}]")
            else:
                cat_color = CATEGORY_COLORS.get(cat.strip().lower(), C.BLUE)
                print(f"\n  {C.BOLD}{cat_color}{cat.upper()}{C.RESET}")
            last_category = cat

        if no_color:
            print(f"  {text}")
        else:
            color = LEVEL_COLORS.get(level, C.RESET)
            print(f"  {color}{text}{C.RESET}")


def run_report(narrator, modules):
    all_messages = []
    json_data = {}

    order = ['uptime', 'system', 'cpu', 'ram', 'disk', 'network', 'temperature', 'processes']
    for mod in order:
        if mod not in modules:
            continue
        if mod == 'uptime':
            msgs = narrator.narrate_uptime()
        elif mod == 'system':
            msgs = narrator.narrate_system_health()
        elif mod == 'cpu':
            msgs = narrator.narrate_cpu()
        elif mod == 'ram':
            msgs = narrator.narrate_memory()
        elif mod == 'disk':
            msgs = narrator.narrate_disk()
        elif mod == 'network':
            msgs = narrator.narrate_network()
        elif mod == 'temperature':
            msgs = narrator.narrate_temperature()
        elif mod == 'processes':
            msgs = narrator.narrate_top_processes()
        else:
            continue

        if msgs:
            all_messages.extend(msgs)
            json_data[mod] = msgs

    return all_messages, json_data


def build_parser():
    parser = argparse.ArgumentParser(
        prog='sysnarrator',
        description='Your Linux system, in plain human language.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sysnarrator                        One-time full report
  sysnarrator --watch                Live dashboard
  sysnarrator --watch --interval 5   Refresh every 5 seconds
  sysnarrator --only cpu,ram         Only CPU and RAM
  sysnarrator --json                 JSON output
  sysnarrator --lang fr              French output
        """
    )
    parser.add_argument('--tui', action='store_true', help='Launch modern interactive TUI dashboard')
    parser.add_argument('--demo', action='store_true', help='Launch interactive TUI in realistic demo simulation mode')
    parser.add_argument('--once', action='store_true', help='Print single static report and exit')
    parser.add_argument('--watch', action='store_true', help='Live dashboard mode')
    parser.add_argument('--interval', type=float, default=3.0, metavar='N', help='Refresh interval in seconds (default: 3)')
    parser.add_argument('--only', type=str, default=None, metavar='MODULES', help=f'Comma-separated: {",".join(ALL_MODULES)}')
    parser.add_argument('--lang', type=str, default='en', choices=['en', 'fr', 'ar'], help='Language (en, fr, ar)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', help='Disable ANSI colors')
    parser.add_argument('--top', type=int, default=5, metavar='N', help='Number of top processes (default: 5)')
    parser.add_argument('--version', action='version', version=f'sysnarrator {__version__}')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    modules = ALL_MODULES
    if args.only:
        modules = [m.strip().lower() for m in args.only.split(',')]
        invalid = [m for m in modules if m not in ALL_MODULES]
        if invalid:
            print(f"Error: unknown modules: {', '.join(invalid)}", file=sys.stderr)
            sys.exit(1)

    narrator = Narrator(lang=args.lang, top_n=args.top)
    no_color = args.no_color or not sys.stdout.isatty()

    if args.json:
        _, json_data = run_report(narrator, modules)
        json_data['timestamp'] = datetime.now().isoformat()
        json_data['hostname'] = os.uname().nodename
        print(json.dumps(json_data, indent=2, ensure_ascii=False))
        return

    # TUI Mode: default when running in an interactive terminal and not requesting --once or --watch
    if args.demo or args.tui or (sys.stdout.isatty() and not args.once and not args.watch):
        from .tui import SysNarratorApp
        app = SysNarratorApp(demo_mode=args.demo)
        app.run()
        return

    if args.watch:
        try:
            while True:
                clear_screen()
                print_dashboard_view(no_color)
                messages, _ = run_report(narrator, modules)
                print_messages(messages, no_color)
                if no_color:
                    print(f"\n  Refreshing every {args.interval}s — Ctrl+C to quit")
                else:
                    print(f"\n  {C.DIM}Refreshing every {args.interval}s — Ctrl+C to quit{C.RESET}")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\nGoodbye! ")
    else:
        print_dashboard_view(no_color)
        messages, _ = run_report(narrator, modules)
        print_messages(messages, no_color)
        print()


if __name__ == '__main__':
    main()
