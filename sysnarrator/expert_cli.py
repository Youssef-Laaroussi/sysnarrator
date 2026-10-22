#!/usr/bin/env python3
"""Professional SysNarrator CLI - Expert System Analysis"""

import argparse
import json
import time
import os
import sys
from datetime import datetime
from . import __version__
from .narrator import Narrator
from .formatters.professional import ProfessionalFormatter
from .expert_analyzer import SystemExpertAnalyzer


class ProfessionalCLI:
    """Professional command-line interface with expert analysis"""

    def __init__(self, args):
        self.args = args
        self.narrator = Narrator(lang=args.lang, top_n=args.top)
        self.no_color = args.no_color or not sys.stdout.isatty()
        self.formatter = ProfessionalFormatter()

    def print_header(self):
        """Print professional header"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostname = os.uname().nodename
        
        header = self.formatter.format_title(f"System Analysis Report - {hostname}")
        print(header)
        
        if not self.no_color:
            print(f"  {self.formatter.Colors.DIM}Generated: {now} | SysNarrator v{__version__}{self.formatter.Colors.RESET}")
        else:
            print(f"  Generated: {now} | SysNarrator v{__version__}")
        
        print()

    def print_system_health(self):
        """Print overall system health score"""
        score = SystemExpertAnalyzer.calculate_health_score()
        print(self.formatter.format_system_score(score, self.no_color))
        print()

    def print_expert_analysis(self):
        """Print expert analysis and recommendations"""
        issues = SystemExpertAnalyzer.get_slowdown_diagnosis(self.args.lang)
        
        if not issues:
            if not self.no_color:
                print(f"  {self.formatter.Colors.GREEN}{self.formatter.Colors.BOLD}✓ System running optimally{self.formatter.Colors.RESET}")
            else:
                print("  ✓ System running optimally")
            return

        print(self.formatter.format_header("EXPERT ANALYSIS", self.no_color))
        
        for issue_type, value in issues:
            if issue_type == 'HIGH_CPU':
                title = "High CPU Usage (>80%)"
                explanation = "CPU saturation causes system slowdowns, heat generation, and battery drain."
                
                if not self.no_color:
                    print(self.formatter.format_expert_tip(
                        title,
                        f"Current: {value:.0f}% - {explanation}",
                        self.no_color
                    ))
                else:
                    print(f"  • {title}: {value:.0f}%")
                    print(f"    {explanation}")
            
            elif issue_type == 'HIGH_MEMORY':
                title = "High RAM Usage (>85%)"
                explanation = "System is using swap memory (100x slower than RAM), causing severe slowdowns."
                
                if not self.no_color:
                    print(self.formatter.format_expert_tip(
                        title,
                        f"Current: {value:.0f}% - {explanation}",
                        self.no_color
                    ))
                else:
                    print(f"  • {title}: {value:.0f}%")
                    print(f"    {explanation}")
            
            elif issue_type == 'HIGH_DISK':
                title = "Critical Disk Space (>90%)"
                explanation = "Insufficient disk space prevents temporary file creation and causes system instability."
                
                if not self.no_color:
                    print(self.formatter.format_expert_tip(
                        title,
                        f"Current: {value:.0f}% - {explanation}",
                        self.no_color
                    ))
                else:
                    print(f"  • {title}: {value:.0f}%")
                    print(f"    {explanation}")
            
            elif issue_type == 'HIGH_TEMP':
                title = "High Temperature (>80°C)"
                explanation = "Elevated temps cause CPU throttling and risk hardware damage. Clean heatsink or replace thermal paste."
                
                if not self.no_color:
                    print(self.formatter.format_expert_tip(
                        title,
                        f"Current: {value:.0f}°C - {explanation}",
                        self.no_color
                    ))
                else:
                    print(f"  • {title}: {value:.0f}°C")
                    print(f"    {explanation}")
            
            elif issue_type == 'HIGH_SWAP':
                title = "High Swap Usage (>30%)"
                explanation = "Using disk memory instead of RAM. System will feel very slow."
                
                if not self.no_color:
                    print(self.formatter.format_expert_tip(
                        title,
                        f"Current: {value:.0f}% - {explanation}",
                        self.no_color
                    ))
                else:
                    print(f"  • {title}: {value:.0f}%")
                    print(f"    {explanation}")

        print()

    def print_detailed_metrics(self):
        """Print detailed system metrics"""
        print(self.formatter.format_header("DETAILED METRICS", self.no_color))
        
        # CPU
        cpu = psutil.cpu_percent(interval=0.5)
        print(self.formatter.format_metric(
            "CPU Usage",
            f"{cpu:.1f}%",
            "",
            "critical" if cpu > 90 else "warning" if cpu > 70 else "ok",
            self.no_color
        ))
        print(self.formatter.format_health_bar(cpu, 30, self.no_color))
        
        # Memory
        mem = psutil.virtual_memory()
        print("\n" + self.formatter.format_metric(
            "RAM Usage",
            f"{mem.used / 1024**3:.1f}GB / {mem.total / 1024**3:.1f}GB",
            f"({mem.percent:.0f}%)",
            "critical" if mem.percent > 90 else "warning" if mem.percent > 75 else "ok",
            self.no_color
        ))
        print(self.formatter.format_health_bar(mem.percent, 30, self.no_color))
        
        # Disk
        disk = psutil.disk_usage('/')
        print("\n" + self.formatter.format_metric(
            "Disk Usage",
            f"{disk.used / 1024**3:.1f}GB / {disk.total / 1024**3:.1f}GB",
            f"({disk.percent:.0f}%)",
            "critical" if disk.percent > 95 else "warning" if disk.percent > 85 else "ok",
            self.no_color
        ))
        print(self.formatter.format_health_bar(disk.percent, 30, self.no_color))
        
        # Swap
        swap = psutil.swap_memory()
        if swap.total > 0:
            print("\n" + self.formatter.format_metric(
                "Swap Usage",
                f"{swap.used / 1024**3:.1f}GB / {swap.total / 1024**3:.1f}GB",
                f"({swap.percent:.0f}%)",
                "warning" if swap.percent > 30 else "ok",
                self.no_color
            ))
            print(self.formatter.format_health_bar(swap.percent, 30, self.no_color))
        
        print()

    def print_top_processes(self):
        """Print top memory-consuming processes with analysis"""
        print(self.formatter.format_header("TOP PROCESSES", self.no_color))
        print(self.formatter.format_divider(no_color=self.no_color))
        
        analysis = SystemExpertAnalyzer.get_top_processes_detail(self.args.top)
        for line in analysis:
            print(f"  {line}")
        
        print()

    def run_professional_report(self):
        """Generate complete professional report"""
        self.print_header()
        self.print_system_health()
        self.print_expert_analysis()
        self.print_detailed_metrics()
        self.print_top_processes()
        
        print(self.formatter.format_divider(char="═", no_color=self.no_color))
        print("  Recommendations applied automatically • For manual optimization see --help")
        print()


def build_professional_parser():
    """Build argument parser for professional CLI"""
    parser = argparse.ArgumentParser(
        prog='sysnarrator-pro',
        description='SysNarrator Professional - Expert System Analysis for Ubuntu',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
PROFESSIONAL ANALYSIS EXAMPLES:
  sysnarrator-pro                    Full expert report with analysis
  sysnarrator-pro --lang fr          Professional report in French
  sysnarrator-pro --lang ar          Professional report in Arabic
  sysnarrator-pro --no-color         Plain text without colors (for logs)
  sysnarrator-pro --json             Structured JSON output

QUICK DIAGNOSIS:
  - System Health Score: 0-100 (higher is better)
  - Red Alert: Issues need immediate attention
  - Yellow Warning: Monitor and address when convenient
  - Green Healthy: System running optimally

For detailed optimization help, see the expert analysis output.
        """
    )
    
    parser.add_argument('--lang', type=str, default='en', 
                       choices=['en', 'fr', 'ar'], 
                       help='Language for analysis output')
    parser.add_argument('--json', action='store_true', 
                       help='Output as JSON')
    parser.add_argument('--no-color', action='store_true', 
                       help='Disable colors (for logging/pipes)')
    parser.add_argument('--top', type=int, default=5, 
                       help='Number of top processes to show')
    parser.add_argument('--version', action='version', 
                       version=f'SysNarrator Professional v{__version__}')
    
    return parser


def main_professional():
    """Main entry point for professional CLI"""
    parser = build_professional_parser()
    args = parser.parse_args()
    
    cli = ProfessionalCLI(args)
    
    if args.json:
        # JSON mode
        data = {
            'timestamp': datetime.now().isoformat(),
            'hostname': os.uname().nodename,
            'version': __version__,
            'health_score': SystemExpertAnalyzer.calculate_health_score(),
        }
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # Professional report mode
        cli.run_professional_report()


# Import for expert analyzer
import psutil

if __name__ == '__main__':
    main_professional()
