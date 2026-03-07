<div align="center">

```
███████╗██╗   ██╗███████╗███╗   ██╗ █████╗ ██████╗ ██████╗  █████╗ ████████╗ ██████╗ ██████╗
██╔════╝╚██╗ ██╔╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████╗ ╚████╔╝ ███████╗██╔██╗ ██║███████║██████╔╝██████╔╝███████║   ██║   ██║   ██║██████╔╝
╚════██║  ╚██╔╝  ╚════██║██║╚██╗██║██╔══██║██╔══██╗██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
███████║   ██║   ███████║██║ ╚████║██║  ██║██║  ██║██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

**Your Linux system, in plain human language.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Ubuntu-orange.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/yourusername/sysnarrator?style=social)]()

> *"Firefox consomme 2.3 Go de RAM depuis 4h — fermer les onglets inactifs libèrerait 800 Mo."*
> Instead of raw numbers, **SysNarrator talks to you like a human would.**

</div>

---

## 🤔 Why SysNarrator?

Every Linux tool — `htop`, `top`, `vmstat`, `iostat` — throws **raw numbers** at you.  
You need to **already know** what those numbers mean to act on them.

**SysNarrator is different.**  
It observes your system, understands the context, and tells you **exactly what's happening and what to do** — in plain language. No jargon. No guessing.

| Classic tools | SysNarrator |
|---|---|
| `CPU: 87%` | `🔥 CPU saturé à 87% — Firefox + VSCode en sont la cause principale` |
| `MEM: 7.2G / 8G` | `🚨 RAM critique (90%) — Slack tourne depuis 6h et fuit de la mémoire` |
| `/dev/sda1: 91%` | `⚠️ Disque à 91% — ~/.cache représente 12 Go, nettoyable facilement` |

---

## ✨ Features

- 🧠 **Human narration** — Every metric becomes a meaningful sentence
- 📊 **Process history** — Tracks how long each app has been running and consuming
- 💡 **Smart suggestions** — Actionable tips, not just observations
- 🌡️ **Temperature monitoring** — With thermal alerts before damage
- 🌐 **Network in plain words** — Real-time + session totals
- 📦 **Multi-format output** — Terminal (colored), JSON, plain text
- 🔄 **Watch mode** — Live dashboard, refreshes every N seconds
- 🌍 **Multi-language** — English 🇬🇧, Français 🇫🇷, العربية 🇲🇦 (and more via contributions)
- 🪶 **Zero bloat** — Only depends on `psutil`, nothing else
- 🐳 **Docker support** — Run in containers too

---

## 📸 Screenshots

```
╔══════════════════════════════════════════════════════════╗
║           SysNarrator  •  14:32:05  •  ubuntu-pc         ║
╠══════════════════════════════════════════════════════════╣
║  CPU                                                     ║
║  ● CPU tranquille à 18% — votre machine respire.         ║
║  ⚙️  Fréquence : 1800 MHz / 4200 MHz max                  ║
║                                                          ║
║  RAM                                                     ║
║  ⚠️  RAM sous pression : 6.1 Go / 8 Go (76%)              ║
║     → Fermez des applications pour libérer de l'espace   ║
║                                                          ║
║  Disque                                                  ║
║  ✅ Disque OK : 45 Go libres sur 256 Go (82% utilisé)    ║
║                                                          ║
║  Réseau                                                  ║
║  🌐 Réseau actif : ↓ 248 Ko/s — ↑ 12 Ko/s               ║
║                                                          ║
║  Top Processus                                           ║
║  1. firefox        (PID  2341)  → 2.1 Go RAM depuis 4h   ║
║  💡 Firefox consomme beaucoup — redémarrer libèrerait     ║
║     de la mémoire.                                       ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🚀 Quick Start

### Install (recommended)

```bash
pip install sysnarrator
```

### From source

```bash
git clone https://github.com/yourusername/sysnarrator.git
cd sysnarrator
pip install -e .
```

### Run

```bash
# One-time report
sysnarrator

# Live dashboard (refresh every 3s)
sysnarrator --watch

# Only RAM + processes
sysnarrator --only ram,processes

# JSON output (for scripts/integrations)
sysnarrator --json

# In French
sysnarrator --lang fr

# In Arabic
sysnarrator --lang ar
```

---

## 📦 Installation Details

### Requirements

| Requirement | Version |
|---|---|
| Python | ≥ 3.10 |
| psutil | ≥ 5.9 |
| Linux kernel | ≥ 4.x |
| Ubuntu/Debian | 20.04+ recommended |

### Supported Distros

| Distro | Status |
|---|---|
| Ubuntu 22.04 / 24.04 | ✅ Fully supported |
| Debian 11 / 12 | ✅ Fully supported |
| Fedora 38+ | ✅ Supported |
| Arch Linux | ✅ Supported |
| Raspberry Pi OS | ✅ Supported |
| macOS | 🔶 Partial (no temperature) |

---

## 🛠️ Usage & Options

```
usage: sysnarrator [-h] [--watch] [--interval N] [--only MODULES]
                   [--lang LANG] [--json] [--no-color] [--version]

  -h, --help          Show this help message
  --watch             Live dashboard mode
  --interval N        Refresh interval in seconds (default: 3)
  --only MODULES      Comma-separated: cpu,ram,disk,network,processes,temp,uptime
  --lang LANG         Language: en, fr, ar (default: en)
  --json              Output as JSON
  --no-color          Disable ANSI colors (for pipes/logs)
  --top N             Show top N processes (default: 5)
  --version           Show version
```

### Examples

```bash
# Monitor only CPU and RAM, refresh every 5s
sysnarrator --watch --interval 5 --only cpu,ram

# Export a system report to JSON
sysnarrator --json > report.json

# Use in a shell script
if sysnarrator --json | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if d['ram']['level']!='critical' else 1)"; then
  echo "System OK"
fi

# Pipe to a log file (no colors)
sysnarrator --no-color >> /var/log/sysnarrator.log
```

---

## 🌍 Internationalization (i18n)

SysNarrator supports multiple languages. Contributions for new languages are very welcome!

```bash
sysnarrator --lang fr   # Français
sysnarrator --lang ar   # العربية
sysnarrator --lang en   # English (default)
```

To add a new language, copy `sysnarrator/i18n/en.json` and translate it. Then open a PR!

---

## 🏗️ Project Structure

```
sysnarrator/
├── sysnarrator/
│   ├── __init__.py          # Package init
│   ├── __main__.py          # Entry point (python -m sysnarrator)
│   ├── cli.py               # Argument parser & main runner
│   ├── narrator.py          # Core narration engine
│   ├── collectors/
│   │   ├── cpu.py           # CPU metrics collector
│   │   ├── memory.py        # RAM & swap collector
│   │   ├── disk.py          # Disk usage & I/O collector
│   │   ├── network.py       # Network I/O collector
│   │   ├── processes.py     # Process tracker with history
│   │   └── temperature.py   # Thermal sensors collector
│   ├── formatters/
│   │   ├── terminal.py      # Colored terminal output
│   │   ├── json_fmt.py      # JSON formatter
│   │   └── plain.py         # Plain text formatter
│   └── i18n/
│       ├── en.json          # English messages
│       ├── fr.json          # French messages
│       └── ar.json          # Arabic messages
├── tests/
│   ├── test_narrator.py
│   ├── test_collectors.py
│   └── test_formatters.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── CONTRIBUTING_TRANSLATIONS.md
├── .github/
│   ├── workflows/
│   │   ├── ci.yml           # Run tests on push
│   │   └── release.yml      # Auto-publish to PyPI
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
└── setup.cfg
```

---

## 🤝 Contributing

Contributions are what make open source amazing. **Any contribution is welcome!**

### Ways to contribute

- 🐛 **Report bugs** — Open an issue with details
- 💡 **Suggest features** — Open a feature request
- 🌍 **Translate** — Add a new language in `sysnarrator/i18n/`
- 🧪 **Write tests** — Improve test coverage
- 📖 **Improve docs** — Fix typos, add examples
- 💻 **Write code** — Pick an issue labeled `good first issue`

### Dev setup

```bash
git clone https://github.com/yourusername/sysnarrator.git
cd sysnarrator
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## 📋 Roadmap

- [x] Core narration engine (CPU, RAM, Disk, Network, Processes)
- [x] Multi-language support (en, fr, ar)
- [x] JSON output
- [x] Watch/live mode
- [ ] Desktop notifications (libnotify)
- [ ] Web dashboard (optional, lightweight)
- [ ] systemd service mode (continuous background monitoring)
- [ ] Alert webhooks (Slack, Discord, Telegram)
- [ ] Plugin system for custom collectors
- [ ] macOS full support
- [ ] Windows Subsystem for Linux (WSL) support
- [ ] `apt` / `snap` / `flatpak` package distribution

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to use, modify, and distribute this software for any purpose.

---

## 🙏 Acknowledgements

- [psutil](https://github.com/giampaolo/psutil) — The backbone of system metrics collection
- The Linux and Ubuntu open source community
- All contributors and translators 💙

---

<div align="center">

**If SysNarrator helped you, give it a ⭐ — it means a lot!**

Made with ❤️ for the Linux community

</div>
