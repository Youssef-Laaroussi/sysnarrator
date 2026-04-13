# SysNarrator Professional
## Expert System Analysis for Ubuntu

**Transform your Linux system diagnostics from raw numbers to professional insights.**

Instead of:
```
CPU: 87% | RAM: 7.2/8GB | Disk: 91%
```

You get:
```
SYSTEM HEALTH SCORE: 72/100 - FAIR
├─ ⚠️ CPU saturated at 87%
├─ 🚨 RAM at 90% (using swap = 100x slower)
└─ 💡 Recommendations: Close Firefox tabs, disable animations, upgrade RAM
```

---

## 🎯 Key Features

### 🔧 **Professional Analysis**
- **System Health Score** (0-100) for quick assessment
- **Expert Diagnosis** with root cause analysis
- **Detailed Metrics** with visual health bars
- **Top Processes** analysis with memory leak detection
- **Smart Recommendations** for optimization

### 💡 **Expert Explanations**
- Why your system is slow
- What's consuming resources
- How to fix problems (step-by-step)
- Ubuntu-specific optimization tips

### 🎨 **Professional Design**
- Modern color scheme (Orange, Blue, Green, Red)
- Clean, readable output with visual hierarchies
- Progress bars and health indicators
- No unnecessary clutter

### 🌍 **Multi-Language**
- **English** — Full analysis and recommendations
- **French (Français)** — Complete expert analysis
- **Arabic (العربية)** — Full support

---

## 📦 Installation

### Using a virtual environment

```bash
cd /home/youssef/sysnarrator
source venv/bin/activate
pip install -e .
```

---

## 🚀 Quick Start

### Basic Professional Report

```bash
sysnarrator
```

Output includes:
- System Health Score (0-100)
- Expert Analysis (what's wrong)
- Detailed Metrics (CPU, RAM, Disk, Swap)
- Top Processes (with leak detection)

### Show Analysis in French

```bash
sysnarrator --lang fr
```

### Output as JSON (for automation)

```bash
sysnarrator --json
```

Note: `--json` outputs JSON only (no terminal UI).

### Plain Text (for logs, no colors)

```bash
sysnarrator --no-color > system_report.txt
```

### Show Top 10 Processes

```bash
sysnarrator --top 10
```

### Live Dashboard (HTOP-style)

```bash
sysnarrator --watch --interval 2
```

---

## 📊 Understanding the Report

### System Health Score

| Score | Status | Meaning |
|-------|--------|---------|
| 90-100 | 🟢 EXCELLENT | System running perfectly |
| 75-89 | 🟢 GOOD | Minor optimizations possible |
| 60-74 | 🟡 FAIR | Some attention recommended |
| 40-59 | 🟠 POOR | Multiple issues to address |
| 0-39 | 🔴 CRITICAL | Immediate action needed |

**How it's calculated:**
- CPU usage penalty: -30 (>90%), -15 (>70%)
- RAM usage penalty: -30 (>90%), -20 (>75%)
- Disk usage penalty: -30 (>95%), -20 (>85%)
- Temperature penalty: -15 (>85°C), -5 (>70°C)

### Detailed Metrics

```
CPU Usage: 45.2%
█████████████░░░░░░░░░░░░░░░░░░ 45% - HEALTHY
```

- **Bars**: CPU (Orange), Mem/Swap (Blue), Disk (Green)
- **Severity**: the percentage value turns Green/Orange/Yellow/Red based on thresholds

### Expert Analysis

When problems are detected:

**High CPU Usage (>80%)**
- Causes: Browser tabs, heavy apps, background processes
- Solutions: Close tabs, check top processes, disable visual effects

**High RAM Usage (>85%)**
- Causes: Memory leaks, too many apps, insufficient RAM
- Solutions: Check processes, close heavy apps, add RAM

**Critical Disk (>90%)**
- Causes: Cache, logs, downloads, large files
- Solutions: Clean cache, remove old logs, archive old files

**High Temperature (>80°C)**
- Causes: Dust, thermal paste degradation, heavy load
- Solutions: Clean heatsink, replace thermal paste, reduce load

---

## 🔧 Advanced Usage

### Continuous Monitoring

```bash
sysnarrator --watch --interval 3
```

### Export Report

```bash
# Save as plain text
sysnarrator --no-color > report.txt

# Save as JSON for automation
sysnarrator --json > report.json

# Create timestamped report
mkdir -p reports
sysnarrator --no-color > reports/$(date +%Y-%m-%d_%H-%M-%S).txt

```

---

## 📋 Interpreting Analysis

### "System running optimally"
✅ No action needed. Everything is healthy.

### Memory Leak Risk
Detected when a single process uses >1000MB and has been running <1 hour.
**Action:** Restart the application to free memory.

### High CPU Alert
Indicates consistent CPU usage >70%.
**Action:** Identify culprit with `top`, close unnecessary apps, disable animations.

### Disk Critical Alert
When disk is >90% full, system becomes unstable.
**Action:**
```bash
# Find large directories
du -sh ~/* | sort -hr | head -10

# Clear cache
rm -rf ~/.cache/tmp/*

# Clean old logs
sudo journalctl --vacuum=3d
```

### Temperature Alert
When CPU >80°C, thermal throttling occurs (automatic slowdown).
**Actions:**
1. Check fan: `pwmconfig` or `lm-sensors`
2. Clean heatsink with compressed air
3. Replace thermal paste (if >3 years old)

---

## 🛠️ Ubuntu Optimization Tips

### Reduce CPU Usage

```bash
# Disable visual effects
Settings → Appearance → Animations: OFF

# Check background services
systemctl list-units --failed

# Disable unnecessary daemons
sudo systemctl disable postgresql  # if not needed
```

### Reduce Memory Usage

```bash
# Clear memory caches
sync && echo 3 > /proc/sys/vm/drop_caches

# Find memory hogs
ps aux --sort=-%mem | head -10

# Reduce browser memory
# Firefox: about:config → browser.tabs.drawInTitlebar → false
```

### Free Up Disk Space

```bash
# Clean package cache
sudo apt clean && sudo apt autoclean

# Remove unused kernels
sudo apt autoremove

# Clear journal logs
sudo journalctl --vacuum=3d

# Find large files
find ~/ -type f -size +100M
```

### Improve Temperature

```bash
# Check thermal sensors
sensors

# Monitor continuously
watch -n 1 sensors

# Clean dust from vents (use compressed air)
# Replace thermal paste (3-5 year interval)
```

---

## 📊 Example Reports

### Healthy System
```
SYSTEM HEALTH SCORE: 95/100 - EXCELLENT
✓ System running optimally

CPU Usage: 22%
RAM Usage: 38% (7.4GB / 19.4GB)
Disk Usage: 65%
Swap Usage: 0%
```

### System Under Load
```
SYSTEM HEALTH SCORE: 65/100 - FAIR

Expert Analysis:
├─ ⚠️  High CPU Usage (>80%)
│   ├─ Cause: Browser with 20+ tabs, VS Code indexing
│   └─ Solutions: Close tabs, disable extensions
│
└─ ⚠️  High RAM Usage (>75%)
    ├─ Cause: Slack, Docker containers, Chrome instances
    └─ Solutions: Close unnecessary tabs, stop Docker
```

### Critical System
```
SYSTEM HEALTH SCORE: 35/100 - CRITICAL

Expert Analysis:
├─ 🔴 CPU saturated at 95%
├─ 🔴 RAM at 92% (using swap = VERY SLOW)
└─ 🔴 Disk at 98% FULL (system unstable)
```

---

## 🔗 Integration

### With System Monitoring Tools

```bash
# Display every 30 seconds in terminal
watch -n 30 'sysnarrator --no-color'

# Pipe to log file
sysnarrator --no-color >> ~/.local/share/sysnarrator.log

# As cron job (hourly report)
0 * * * * cd /home/youssef/sysnarrator && source venv/bin/activate && sysnarrator --no-color >> ~/reports/system.log
```

### With Scripts

```bash
#!/bin/bash
# Auto-cleanup when disk >80%

# Note: SysNarrator JSON is narrative messages (human text). For numeric automation,
# use standard tools like df.
used_pct=$(df -P / | awk 'NR==2{gsub(/%/,"",$5); print $5}')

if [ "$used_pct" -gt 80 ]; then
    sudo apt clean
    sudo journalctl --vacuum=3d
    rm -rf ~/.cache/tmp/*
fi
```

---

## 🎨 Color Scheme

**Professional Color Palette:**
- 🟠 **Orange** — CPU bars and emphasis
- 🔵 **Blue** — Memory/Swap bars and information
- 🟢 **Green** — OK status and Disk bar
- 🟡 **Yellow** — Warning severity
- 🔴 **Red** — Critical severity

---

## 📚 Additional Commands

```bash
# Help
sysnarrator --help

# Test different languages
sysnarrator --lang en  # English
sysnarrator --lang fr  # French
sysnarrator --lang ar  # Arabic

# No output colors (for scripts)
sysnarrator --no-color
```

---

## 🤝 Support & Contribution

### Report Issues
If you find a bug or inaccuracy in analysis:
```bash
sysnarrator --no-color > ~/bug_report.txt
# Share the output in an issue
```

### Add Analysis
Want to add more expert recommendations?
```bash
# Edit expert patterns in sysnarrator/expert_analyzer.py
nano sysnarrator/expert_analyzer.py
```

---

## 📖 Understanding Linux Performance

### Key Metrics Explained

**CPU %**: Current processor utilization
- <20%: Idle
- 20-50%: Normal
- 50-80%: High activity
- >80%: Bottleneck risk

**RAM %**: Physical memory in use
- <50%: Plenty of headroom
- 50-75%: Normal operation
- 75-90%: Getting tight, monitor swap
- >90%: Swap being used = SLOW

**Disk %**: Disk space used
- <70%: Healthy
- 70-85%: Monitor
- >85%: Start cleanup
- >95%: CRITICAL, system unstable

**Swap %**: Virtual memory (disk-based RAM)
- 0%: Ideal
- <10%: Normal
- 10-30%: Monitor
- >30%: System very slow

**Temperature**: CPU heat in Celsius
- <60°C: Cool
- 60-75°C: Normal
- 75-85°C: Hot, monitor
- >85°C: Throttling occurs, reduce load

---

## 📝 License

MIT License - See LICENSE file for details

---

**Make your system fast again. Get expert advice, not just metrics.**

*SysNarrator Professional v0.1.0 — Professional Ubuntu System Analysis*
