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

LEVEL_COLORS = {
    'critical': C.RED,
    'warning':  C.YELLOW,
    'ok':       C.GREEN,
    'info':     C.CYAN,
}

ALL_MODULES = ['cpu', 'ram', 'disk', 'network', 'processes', 'temperature', 'uptime']


def clear_screen():
    os.system('clear')


def print_header(no_color=False):
    now = datetime.now().strftime("%H:%M:%S")
    hostname = os.uname().nodename
    version = f"v{__version__}"
    if no_color:
        print(f"{'═'*60}")
        print(f"  SysNarrator {version}  •  {now}  •  {hostname}")
        print(f"{'═'*60}")
    else:
        print(f"{C.CYAN}{'═'*60}{C.RESET}")
        print(f"  {C.BOLD}{C.WHITE}SysNarrator{C.RESET} {C.DIM}{version}{C.RESET}  {C.DIM}•{C.RESET}  {C.CYAN}{now}{C.RESET}  {C.DIM}•{C.RESET}  {C.MAGENTA}{hostname}{C.RESET}")
        print(f"{C.CYAN}{'═'*60}{C.RESET}")


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
                print(f"\n  {C.BOLD}{C.WHITE}{cat.upper()}{C.RESET}")
            last_category = cat

        if no_color:
            print(f"  {text}")
        else:
            color = LEVEL_COLORS.get(level, C.RESET)
            print(f"  {color}{text}{C.RESET}")


def run_report(narrator, modules):
    all_messages = []
    json_data = {}

    order = ['uptime', 'cpu', 'ram', 'disk', 'network', 'temperature', 'processes']
    for mod in order:
        if mod not in modules:
            continue
        if mod == 'uptime':
            msgs = narrator.narrate_uptime()
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

    if args.watch:
        try:
            while True:
                clear_screen()
                print_header(no_color)
                messages, _ = run_report(narrator, modules)
                print_messages(messages, no_color)
                if no_color:
                    print(f"\n  Refreshing every {args.interval}s — Ctrl+C to quit")
                else:
                    print(f"\n  {C.DIM}Refreshing every {args.interval}s — Ctrl+C to quit{C.RESET}")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
    else:
        print_header(no_color)
        messages, _ = run_report(narrator, modules)
        print_messages(messages, no_color)
        print()


if __name__ == '__main__':
    main()
