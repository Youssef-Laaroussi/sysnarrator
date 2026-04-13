# SysNarrator Architecture

## Overview

**SysNarrator** is a Linux system monitoring tool that transforms raw system metrics into human-readable narratives. Instead of displaying raw numbers like "CPU: 87%", it provides contextual information: "CPU saturated at 87% — system is under extreme pressure."

The architecture is designed around a **modular collector-narrator-formatter pipeline**, allowing for easy extension and testing.

---

## Core Architecture

### 1. **Data Collection Layer** (`collectors/`)

Provides specialized collectors for different system resources:

```
collectors/
├── cpu.py           → CPU metrics (usage, frequency, cores)
├── memory.py        → RAM & swap usage
├── disk.py          → Disk space & I/O metrics
├── network.py       → Network interfaces & bandwidth
├── processes.py     → Process listing & resource usage
└── temperature.py   → Thermal sensors (if available)
```

Each collector is a static utility class with methods for retrieving specific metrics:

```python
# Example usage
from sysnarrator.collectors.cpu import CPUCollector
cpu_percent = CPUCollector.get_overall_percent()
frequencies = CPUCollector.get_frequency()
```

**Design**: Collectors are **read-only**, stateless modules. They abstract away `psutil` API details and provide consistent interfaces.

---

### 2. **Narration Engine** (`narrator.py`)

The core `Narrator` class transforms metrics into human-readable messages.

#### Key Responsibilities:
- **Data collection** — Direct psutil calls (could be refactored to use collectors)
- **Analysis** — Interprets metrics and determines severity levels
- **Translation** — Applies language-specific messages via templating
- **History tracking** — Maintains process history for duration calculation

#### Core Methods:

| Method | Purpose |
|--------|---------|
| `narrate_cpu()` | CPU usage analysis with thermal alerts |
| `narrate_memory()` | RAM/swap analysis with pressure indicators |
| `narrate_disk()` | Disk space warnings and capacity analysis |
| `narrate_network()` | Current bandwidth + session totals |
| `narrate_temperature()` | Thermal sensor monitoring |
| `narrate_uptime()` | System uptime tracking |
| `narrate_top_processes()` | Top RAM consumers with suggestions |

#### Message Levels:
- **critical** 🔴 — Immediate action needed (e.g., CPU >90%)
- **warning** 🟡 — Degradation possible (e.g., RAM >75%)
- **info** 🔵 — Informational (e.g., mode details)
- **ok** 🟢 — System healthy (e.g., CPU <40%)

#### Formatting Utilities:
```python
narrator._fmt_bytes(1500)      # → "1.5 GB"
narrator._fmt_duration(120)    # → "2h"
narrator._msg('cpu_critical', pct=87)  # → Translated message
```

---

### 3. **Output Formatting Layer** (`formatters/`)

Handles different output formats:

```
formatters/
├── terminal.py      → ANSI-colored terminal output
├── json_fmt.py      → Machine-readable JSON
└── plain.py         → Plain text (no colors)
```

#### Terminal Formatter
```python
from sysnarrator.formatters.terminal import TerminalFormatter
colored_output = TerminalFormatter.format_messages(messages, no_color=False)
```

#### JSON Formatter
```python
from sysnarrator.formatters.json_fmt import JSONFormatter
json_str = JSONFormatter.to_json_string(report, indent=2)
```

**Design**: Formatters are stateless and handle output presentation only. They don't modify message content.

---

### 4. **CLI Interface** (`cli.py`)

Provides command-line argument parsing and orchestration.

#### Key Components:
- **Argument Parser** — Defined in `build_parser()`
- **Report Runner** — `run_report()` orchestrates collector and narrator calls
- **Display Handler** — `print_messages()` formats and outputs results
- **Watch Mode** — Continuous monitoring with configurable refresh intervals

#### Main Entry Points:
```bash
# One-time report
sysnarrator --no-color

# Live dashboard
sysnarrator --watch --interval 5

# JSON output
sysnarrator --json

# Language selection
sysnarrator --lang fr
```

---

## Data Flow

```
┌──────────────────────────┐
│  CLI Arguments Parser    │
│  (cli.build_parser)      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Narrator (narrator.py)  │
│  - Data collection       │
│  - Analysis              │
│  - Message generation    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Message List            │
│  [{level, text, cat}, ...] │
└────────────┬─────────────┘
             │
      ┌──────┴──────────┬────────────┐
      ▼                 ▼            ▼
┌─────────────┐ ┌──────────────┐ ┌────────────┐
│Terminal     │ │JSONFormatter │ │PlainFormat │
│Formatter    │ │              │ │            │
└─────────────┘ └──────────────┘ └────────────┘
      │                 │            │
      └────────────┬────┴───┬────────┘
                   ▼        ▼
            ┌─────────────────────────┐
            │  Display Output         │
            │  (Terminal/JSON/File)   │
            └─────────────────────────┘
```

---

## Language Support & Internationalization

Messages stored in `i18n/` as JSON files:

```
i18n/
├── en.json  → English messages
├── fr.json  → French (Français)
└── ar.json  → Arabic (العربية)
```

The `MESSAGES` dictionary in `narrator.py` contains all locale templates:

```python
MESSAGES['en']['cpu_critical'] = '🔥 CPU saturated at {pct:.0f}%...'
MESSAGES['fr']['cpu_critical'] = '🔥 CPU saturé à {pct:.0f}%...'
```

Language selection at initialization:
```python
narrator = Narrator(lang='fr')  # French output
```

---

## Testing Strategy

Test coverage in `tests/`:

| Test File | Coverage |
|-----------|----------|
| `test_narrator.py` | Core narration logic, message formatting, language support |
| `test_collectors.py` | (Planned) Collector module functionality |
| `test_formatters.py` | (Planned) Output formatter correctness |

### Running Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=sysnarrator

# Specific test file
pytest tests/test_narrator.py -v
```

---

## Key Design Decisions

### 1. **Monolithic Narrator vs. Modular Collectors**
Currently, the `Narrator` class directly calls `psutil` for data collection. The separate `collectors/` modules provide an abstraction layer for future refactoring and testing.

**Future improvement**: Refactor `Narrator` to use collectors:
```python
def narrate_cpu(self):
    pct = CPUCollector.get_overall_percent()
    # ... analyze and narrate
```

### 2. **Message Templates Over String Formatting**
Messages are stored as templates (e.g., `"CPU at {pct}%"`) to support:
- Multiple languages easily
- Consistent placeholders
- Easy content updates without code changes

### 3. **Severity Levels (critical/warning/ok/info)**
Each message includes a `level` for:
- Color coding in terminal
- Severity filtering in JSON
- Alerting integrations (future)

### 4. **Process History Tracking**
The `ProcessHistory` class maintains a 30-minute rolling window of process metrics to enable:
- Accurate duration reporting
- Trend detection (coming soon)
- Smart suggestions ("restarting Firefox could free 800 MB")

### 5. **Language-Agnostic Data**
Narration logic separates:
- **Data calculation** (percentage, bytes, etc.) — Language-independent
- **Presentation** (message templates, units) — Language-dependent

This allows easy addition of new languages without code changes.

---

## Extension Points

### Adding a New Language
1. Copy `i18n/en.json` to `i18n/[lang].json`
2. Translate all values (keep keys in English)
3. Update `Narrator.__init__()` to support the language
4. Test: `Narrator(lang='es')`

### Adding a New Metric
1. Create collection logic (use existing collectors or add new one)
2. Create narration method in `Narrator` class
3. Add message templates to `MESSAGES['en']`, `['fr']`, `['ar']`
4. Add to CLI in `cli.py:run_report()`
5. Add corresponding tests

### Custom Output Format
1. Create new formatter in `formatters/`
2. Implement `format_messages()` method
3. Register in `cli.py` argument parsing

---

## Dependencies

- **psutil** ≥ 5.9 — System metrics collection
- **pytest** (dev) — Testing framework
- **pytest-cov** (dev) — Coverage reporting
- **flake8** (dev) — Code linting

No external dependencies for core functionality (minimal bloat, maximum portability).

---

## Performance Considerations

- **CPU measurement** — 0.5s sampling window (affects first call)
- **Network measurement** — 1s delta calculation
- **Process iteration** — psutil iteration is optimized internally
- **History window** — 30-minute rolling window with automatic pruning
- **Watch mode** — Configurable refresh interval (default 3s)

### Memory Footprint
- Baseline: ~20 MB
- Process history scales with number of processes (typical max 500 processes = ~5 MB additional)

---

## Security & Permissions

- Some metrics require elevated privileges (e.g., temperature sensors)
- Code gracefully handles `PermissionError` and `AccessDenied` exceptions
- No sensitive data is collected or exposed

---

## Known Limitations

- **macOS** — Limited temperature support (no `/sys/class/thermal` equivalent)
- **Windows** — Not supported (uses Linux-only APIs)
- **Temperature sensor availability** — Varies by hardware
- **Network per-interface stats** — May require elevated privileges

---

## Future Roadmap

- [ ] Desktop notifications (libnotify)
- [ ] Web dashboard (lightweight, optional)
- [ ] systemd service mode
- [ ] Alert webhooks (Slack, Discord, Telegram)
- [ ] Plugin system for custom collectors
- [ ] Performance metrics (disk I/O, context switches)
- [ ] Historical trending & graphs
- [ ] Configuration file support

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup and guidelines.

---

*Last updated: 2026-04-03*
