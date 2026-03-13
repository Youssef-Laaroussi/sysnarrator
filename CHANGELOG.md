# Changelog

All notable changes to SysNarrator will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Nothing yet — be the first to contribute!

---

## [0.1.0] — 2026-03-13

### Added
- 🎉 Initial release
- Core narration engine: CPU, RAM, Disk, Network, Processes, Temperature, Uptime
- Colored terminal output with severity levels (critical, warning, ok, info)
- JSON output mode (`--json`)
- Live watch mode (`--watch`) with configurable refresh interval
- Multi-language support: English (`en`), French (`fr`), Arabic (`ar`)
- `--only` flag to select specific modules
- `--top N` flag to control number of processes shown
- `--no-color` flag for piping and log files
- Process history tracker — duration and average RAM/CPU per process
- Smart suggestions (e.g. "restarting Firefox could free 800 MB")
- Thermal sensor monitoring with critical alerts
- Swap usage analysis
- Network session totals and real-time bandwidth

---

[Unreleased]: https://github.com/Youssef-Laaroussi/sysnarrator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Youssef-Laaroussi/sysnarrator/releases/tag/v0.1.0
