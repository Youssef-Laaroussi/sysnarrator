# SysNarrator Professional Interface

## HTOP-Style Visual Features

### 1. Real-time Resource Bars
SysNarrator now displays beautiful HTOP-style resource bars with dynamic coloring:

```
  CPU      [███████░░░░░░░░░░░░░░░]  57.2%
  Mem      [██████████░░░░░░░░░░░░]  41.8%
  Swp      [░░░░░░░░░░░░░░░░░░░░░░░]   0.0%
```

**Color Coding:**
- 🟢 Green: < 50% usage (healthy)
- 🟠 Orange: 50-75% usage (elevated)
- 🟡 Yellow: 75-90% usage (warning)
- 🔴 Red: ≥ 90% usage (critical)

### 2. System Health Score (0-100)
Comprehensive health assessment combining:
- CPU pressure metrics
- Memory utilization
- Disk space availability
- Temperature readings
- Process memory leak detection

```
✨ System Health: 95/100 — Excellent, running optimally
💚 System Health: 78/100 — Good, minor issues
💛 System Health: 65/100 — Fair, attention needed
❌ System Health: 42/100 — Poor, critical action required
```

### 3. Advanced Process Monitoring
- Top N RAM-consuming processes
- Memory leak detection with confidence scoring
- CPU per-process tracking
- Process uptime tracking
- Visual leak indicator: ⚠️ LEAK (XX%)

```
🔍 Top 5 RAM-hungry processes:
  1. chrome           (PID   8741)  → 946 MB for less than a minute
  2. code             (PID  22134)  → 683 MB for less than a minute | CPU 21%
  3. mysqld           (PID   2058)  → 388 MB ⚠️ LEAK (68%)
```

### 4. Predictive Analytics
**Disk Full Prediction:**
- Analyzes 30-minute disk usage trends
- Predicts when disk will reach capacity
- Alerts for short-term critical conditions (< 48 hours)

```
📈 Disk filling up: will be full in 18.5 hours at current rate.
```

### 5. Multilingual Support
Complete support for:
- 🇬🇧 English
- 🇫🇷 Français (French)
- 🇸🇦 العربية (Arabic)

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

## Features Beyond HTOP

✅ **Human-Readable Narration**
- Natural language descriptions of system state
- Conversational tone with emojis
- Contextual recommendations

✅ **Intelligent Alerts**
- Memory leak detection with ML-style pattern matching
- Thermal warnings
- Swap space monitoring
- Network activity analysis

✅ **Historical Trend Analysis**
- Long-term system behavior tracking
- 1-hour trend window for deep analysis
- CPU frequency monitoring
- Disk usage extrapolation

✅ **Predictive Maintenance**
- Disk full predictions
- Memory pressure forecasting
- Thermal trend analysis

✅ **Professional Reporting**
- Structured JSON output for monitoring systems
- Category-based message organization
- Severity levels (ok, info, warning, critical)

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

## Architecture

- **Collector Pattern**: Modular collectors for each system metric
- **Narrator Pattern**: Intelligent analysis and message generation
- **Formatter Pattern**: Multiple output formats (terminal, JSON, professional)
- **ProcessHistory**: Advanced analytics for process tracking
- **Trend Analysis**: Historical data processing for predictions

## Performance

- Minimal dependencies (psutil only)
- Efficient 1-hour rolling buffer for trend analysis
- Fast process enumeration
- Real-time responsive UI updates

## Status Bar Colors

The colored bars automatically match terminal capabilities and use ANSI 256-color codes:
- Orange: 38;5;208m (CPU usage)
- Blue: 38;5;33m (Secondary info)
- Green: 38;5;76m (Healthy status)
- Red: 38;5;196m (Critical alerts)
