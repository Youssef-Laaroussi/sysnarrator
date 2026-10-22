# SysNarrator Professional Interface

## Visual Dashboard Features

### 1. Real-time Resource Bars
SysNarrator displays dynamic visual resource bars with color-coded severity:

```text
  CPU      [███████░░░░░░░░░░░░░░░]  57.2%
  Mem      [██████████░░░░░░░░░░░░]  41.8%
  Swp      [░░░░░░░░░░░░░░░░░░░░░░░]   0.0%
```

**Color Coding:**
- Green: < 50% usage (healthy)
- Orange: 50-75% usage (elevated)
- Yellow: 75-90% usage (warning)
- Red: ≥ 90% usage (critical)

### 2. System Health Score (0-100)
Comprehensive health assessment combining:
- CPU pressure metrics
- Memory utilization
- Disk space availability
- Temperature readings
- Process memory leak detection

```text
System Health: 95/100 — Excellent, running optimally
System Health: 78/100 — Good, minor issues
System Health: 65/100 — Fair, attention needed
System Health: 42/100 — Poor, critical action required
```

### 3. Advanced Process Monitoring
- Top N RAM-consuming processes
- Memory leak detection with confidence scoring
- CPU per-process tracking
- Process uptime tracking
- Visual leak indicator: LEAK (XX%)

```text
Top 5 RAM-hungry processes:
  1. chrome           (PID   8741)  → 946 MB for less than a minute
  2. code             (PID  22134)  → 683 MB for less than a minute | CPU 21%
  3. mysqld           (PID   2058)  → 388 MB LEAK (68%)
```

### 4. Predictive Analytics
**Disk Full Prediction:**
- Analyzes 30-minute disk usage trends
- Predicts when disk will reach capacity
- Alerts for short-term critical conditions (< 48 hours)

```text
Disk filling up: will be full in 18.5 hours at current rate.
```

### 5. Multilingual Support
Complete support for:
- English
- Français (French)
- العربية (Arabic)

### 6. Multiple Output Formats

**Terminal (Default):**
```bash
sysnarrator
```

**Watch Mode (Live Dashboard):**
```bash
sysnarrator --watch --interval 3
```

**JSON Export:**
```bash
sysnarrator --json
```

**Filtered Reports:**
```bash
sysnarrator --only cpu,ram,disk
sysnarrator --top 10        # Show top 10 processes
```

**Language Selection:**
```bash
sysnarrator --lang fr
sysnarrator --lang ar
```

**Plain Text (No Colors):**
```bash
sysnarrator --no-color
```

## Features Beyond Traditional Tools

| Feature | Classic Tools | `SysNarrator` |
|---|---|---|
| **Interpretation** | Raw numbers only | Full natural language narration |
| **Linux OS Background** | Minimal (Uptime, hostname) | Complete Distro, Kernel, Desktop Environment, Architecture |
| **Zombie / D-state Detection** | Passive letter state (`Z`, `D`) | Proactive detection with alert and PIDs |
| **Disk I/O Throughput** | Missing | Built-in real-time Read/Write MB/s throughput |
| **Load vs Cores Context** | Raw 1/5/15 load values | Computes true core saturation percentage |
| **Predictive Warnings** | None | Disk-full countdown & memory leak scoring |
| **Actionable Suggestions** | None | Actionable commands and remediation tips |
| **Battery & Power** | None | Battery %, charge state, and time remaining |

- **Human-Readable Narration**: Natural language descriptions of system state, root cause diagnosis and contextual recommendations.
- **Deep Linux Environment & Task Accounting**: Linux distribution identification (Ubuntu, Debian, Fedora, Arch, etc.), Kernel version, CPU architecture, Desktop session, real-time task states, and proactive alerts for zombie processes and uninterruptible D-state I/O hangs.
- **Disk I/O Rate Tracking**: Real-time read and write throughput in MB/s with heavy flush detection.
- **Intelligent Alerts & Predictive Analysis**: Memory leak detection with confidence scoring, predictive disk exhaustion countdown, and thermal throttling warnings.

## Command Examples

```bash
# One-time full report
sysnarrator

# Live dashboard, refresh every 2 seconds, French
sysnarrator --watch --interval 2 --lang fr

# Only CPU and RAM, no colors
sysnarrator --only cpu,ram --no-color

# Top 10 processes, JSON output
sysnarrator --top 10 --json

# System health check in Arabic
sysnarrator --lang ar --only system

# Continuous monitoring
sysnarrator --watch
```
