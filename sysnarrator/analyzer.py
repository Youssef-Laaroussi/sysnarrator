"""
Expert System - Detailed Analysis & Recommendations for Ubuntu
Provides in-depth explanations and professional recommendations.
"""

import psutil
import time


class SystemExpertAnalyzer:
    """
    Advanced system analysis with expert recommendations.
    Provides detailed explanations in English, French, and Arabic.
    """

    EXPERT_TIPS = {
        'en': {
            'high_cpu': {
                'title': 'High CPU Usage Detected',
                'explanation': 'CPU usage above 80% indicates system stress. This can cause slowdowns, heat generation, and reduced battery life.',
                'causes': [
                    'Background applications consuming resources',
                    'Unoptimized software running multiple processes',
                    'Browser with too many tabs open',
                    'Large file operations (encoding, compression)',
                    'Virtual machines running simultaneously',
                ],
                'solutions': [
                    'Close unnecessary browser tabs (each tab uses 50-100 MB RAM + CPU)',
                    'Use "top" or "ps aux" to identify CPU-hungry processes',
                    'Disable unnecessary startup services: systemctl list-units --failed',
                    'Update packages: sudo apt update && sudo apt upgrade',
                    'Reduce visual effects: Settings → Appearance → Less animations',
                ],
            },
            'high_memory': {
                'title': 'High RAM Usage Detected',
                'explanation': 'RAM usage above 75% forces system to use swap (disk memory), which is 100x slower than physical RAM. This causes severe slowdowns.',
                'causes': [
                    'Memory leaks in running applications',
                    'Too many browser tabs or background processes',
                    'RAM-intensive applications (IDEs, VMs, Docker containers)',
                    'Caching accumulation over time',
                ],
                'solutions': [
                    'Clear memory caches: sync && echo 3 > /proc/sys/vm/drop_caches',
                    'Check top memory users: ps aux --sort=-%mem | head -10',
                    'Reduce browser memory: Install "One Tab" or "The Great Suspender"',
                    'Close memory-heavy applications (Slack, Discord, Zoom)',
                    'Consider upgrading RAM if consistently high',
                    'Disable heavy desktop effects temporarily',
                ],
            },
            'high_disk': {
                'title': 'Disk Space Critical',
                'explanation': 'When disk is >85% full, system becomes unstable. Insufficient space prevents temporary file creation, log operations, and can cause data corruption.',
                'causes': [
                    'Large cache directories (~/.cache, /tmp)',
                    'Old log files accumulation (/var/log)',
                    'Download folder overflow',
                    'Duplicate files and backups',
                    'Large media files not organized',
                ],
                'solutions': [
                    'Find large directories: du -sh ~/* | sort -hr | head -10',
                    'Clear package cache: sudo apt clean && sudo apt autoclean',
                    'Clean old logs: sudo journalctl --vacuum=3d',
                    'Clear temporary files: rm -rf ~/.cache/tmp/* (careful!)',
                    'Use Disk Usage Analyzer: baobab',
                    'Uninstall unused packages: sudo apt autoremove',
                ],
            },
            'high_temperature': {
                'title': 'System Temperature Elevated',
                'explanation': 'High temperatures cause CPU throttling (performance reduction), hardware degradation, and risk of permanent damage. Thermal paste degrades ~5% per year.',
                'causes': [
                    'Dust buildup in heatsink blocking airflow',
                    'Thermal paste dried out (3-5 years old)',
                    'Fan not spinning or low speed',
                    'Ambient temperature too high',
                    'Overclocking or heavy sustained load',
                ],
                'solutions': [
                    'Check fan status: pwmconfig or lm-sensors',
                    'Increase cooling: Clean dust from vents with compressed air',
                    'Monitor actual temps: watch -n 1 sensors',
                    'Apply thermal paste if overheating persists (professional service)',
                    'Reduce sustained workloads until cooling improves',
                    'Use cooling pad if laptop (temporary solution)',
                    'Check BIOS for fan curves',
                ],
            },
            'slow_disk': {
                'title': 'Slow Disk I/O Performance',
                'explanation': 'Slow disk access makes entire system feel unresponsive. Affects boot time, application startup, and file transfers. HDD degradation or heavy I/O can cause this.',
                'causes': [
                    'Mechanical HDD reaching end-of-life (wear after 5-10 years)',
                    'Too many processes reading/writing simultaneously',
                    'Disk fragmentation (on HDD, not SSD)',
                    'Background indexing or virus scanning',
                    'Failing hard drive (SMART errors)',
                ],
                'solutions': [
                    'Check disk health: sudo smartctl -a /dev/sda',
                    'Monitor disk I/O: iostat -x 1 5',
                    'Identify heavy I/O: iotop (install: sudo apt install iotop)',
                    'Upgrade to SSD (most effective: 10x faster than HDD)',
                    'Defragment HDD (if not SSD): e4defrag /dev/sda',
                    'Disable search indexing if not needed: dconf-editor → org.gnome.desktop.search-providers',
                ],
            },
            'slow_network': {
                'title': 'Network Performance Issues',
                'explanation': 'Slow network affects cloud apps, updates, streaming, and file transfers. Can indicate ISP issues, interference, or network congestion.',
                'causes': [
                    'WiFi interference from microwave, cordless phones (2.4 GHz)',
                    'Too far from router (signal strength <-70 dBm is poor)',
                    'Excessive background downloads (updates, sync)',
                    'Neighbor networks on same WiFi channel',
                    'DNS resolution delays',
                    'ISP throttling or congestion',
                ],
                'solutions': [
                    'Test speed: speedtest-cli or ookla speedtest',
                    'Check WiFi signal: nmcli dev wifi',
                    'Switch WiFi to 5GHz band (if available, less interference)',
                    'Change WiFi channel: Use WiFi analyzer, pick less used channel',
                    'Move closer to router or use Ethernet cable',
                    'Change DNS: Use 1.1.1.1 (Cloudflare) or 8.8.8.8 (Google)',
                    'Stop background downloads: Check Software Updater settings',
                ],
            },
        },
        'fr': {
            'high_cpu': {
                'title': 'Utilisation CPU Élevée Détectée',
                'explanation': 'CPU > 80% indique une saturation système. Cause des ralentissements, génère de la chaleur, réduit l\'autonomie batterie.',
                'causes': [
                    'Applications d\'arrière-plan consommant ressources',
                    'Logiciels non optimisés avec multiples processus',
                    'Navigateur avec trop d\'onglets',
                    'Opérations sur fichiers volumineux',
                    'Machines virtuelles tournant simultanément',
                ],
                'solutions': [
                    'Fermer onglets inutiles (chaque onglet = 50-100 MB RAM)',
                    'Identifier processus gourmands: top ou ps aux',
                    'Désactiver services inutiles: systemctl list-units --failed',
                    'Mettre à jour: sudo apt update && sudo apt upgrade',
                    'Réduire effets visuels: Paramètres → Apparence → Animations',
                ],
            },
            'high_memory': {
                'title': 'Utilisation RAM Élevée',
                'explanation': 'RAM > 75% force le système à utiliser le SWAP (mémoire disque), 100x plus lent. Cause des ralentissements sévères.',
                'causes': [
                    'Fuites mémoire dans applications',
                    'Trop d\'onglets navigateur ou processus',
                    'Applications gourmandes (IDE, VM, Docker)',
                    'Accumulation cache',
                ],
                'solutions': [
                    'Vider cache mémoire: sync && echo 3 > /proc/sys/vm/drop_caches',
                    'Voir processus RAM: ps aux --sort=-%mem | head -10',
                    'Réduire RAM navigateur: Extension "One Tab"',
                    'Fermer apps lourdes (Slack, Discord, Zoom)',
                    'Envisager upgrade RAM si persistant',
                ],
            },
        },
    }

    @staticmethod
    def get_top_processes_detail(n=5):
        """Get detailed information about top memory-consuming processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'create_time']):
            try:
                ram_mb = proc.info['memory_info'].rss / 1024 / 1024
                runtime = time.time() - proc.info['create_time']
                runtime_hours = runtime / 3600
                
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'ram_mb': ram_mb,
                    'cpu_percent': proc.info['cpu_percent'],
                    'runtime_hours': runtime_hours,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        sorted_procs = sorted(processes, key=lambda x: x['ram_mb'], reverse=True)[:n]
        
        analysis = []
        total_ram = sum(p['ram_mb'] for p in sorted_procs)
        
        for p in sorted_procs:
            impact = (p['ram_mb'] / total_ram * 100) if total_ram > 0 else 0
            
            msg = f"{p['name']}: {p['ram_mb']:.0f}MB ({impact:.1f}% of top {n})"
            if p['ram_mb'] > 1000:
                msg += " [MEMORY LEAK RISK - Restarting app recommended]"
            elif p['cpu_percent'] > 50:
                msg += f" [HIGH CPU: {p['cpu_percent']:.1f}%]"
            
            analysis.append(msg)
        
        return analysis

    @staticmethod
    def get_disk_analysis():
        """Get detailed disk usage analysis"""
        import subprocess
        
        analysis = {
            'large_dirs': [],
            'cache_size': 0,
            'logs_size': 0,
        }
        
        # Cache analysis
        try:
            result = subprocess.run(
                ['du', '-sh', os.path.expanduser('~/.cache')],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                size = result.stdout.split()[0]
                analysis['cache_size'] = size
        except:
            pass

        return analysis

    @staticmethod
    def calculate_health_score():
        """
        Calculate overall system health score (0-100).
        Based on CPU, memory, disk, temperature.
        """
        score = 100
        
        # CPU penalty
        cpu = psutil.cpu_percent(interval=1)
        if cpu > 90:
            score -= 30
        elif cpu > 70:
            score -= 15
        elif cpu > 50:
            score -= 5
        
        # Memory penalty
        mem = psutil.virtual_memory()
        if mem.percent > 90:
            score -= 30
        elif mem.percent > 75:
            score -= 20
        elif mem.percent > 60:
            score -= 10
        
        # Disk penalty
        disk = psutil.disk_usage('/')
        if disk.percent > 95:
            score -= 30
        elif disk.percent > 85:
            score -= 20
        elif disk.percent > 70:
            score -= 10
        
        # Temperature penalty (if available)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for chip, sensors in temps.items():
                    for sensor in sensors:
                        if sensor.current and sensor.current > 0:
                            if sensor.current > 85:
                                score -= 15
                            elif sensor.current > 70:
                                score -= 5
        except:
            pass
        
        return max(0, min(100, score))

    @staticmethod
    def get_slowdown_diagnosis(lang='en'):
        """
        Diagnose main causes of system slowdown.
        Returns list of key issues with recommendations.
        """
        issues = []
        
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        swap = psutil.swap_memory()
        
        # CPU Issues
        if cpu > 80:
            issues.append(('HIGH_CPU', cpu))
        
        # Memory Issues
        if mem.percent > 85:
            issues.append(('HIGH_MEMORY', mem.percent))
        elif swap.percent > 30:
            issues.append(('HIGH_SWAP', swap.percent))
        
        # Disk Issues
        if disk.percent > 90:
            issues.append(('HIGH_DISK', disk.percent))
        
        # Temperature Issues
        try:
            temps = psutil.sensors_temperatures()
            max_temp = 0
            for chip, sensors in temps.items():
                for sensor in sensors:
                    if sensor.current:
                        max_temp = max(max_temp, sensor.current)
            if max_temp > 80:
                issues.append(('HIGH_TEMP', max_temp))
        except:
            pass
        
        return issues


# Utility import
import os
