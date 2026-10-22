# SysNarrator Design Specification (Original Identity)

## 1. Distinctive Concept: "A System Dashboard That Talks"
SysNarrator is neither a process list nor a raw bar wall. Its hero is the **System Health Command Center**, integrating:
1. **Health Score & Narration First**: Plain-language real-time insights, explainable 0-100 score.
2. **Telemetry Without Clones**: Braille/Block gradient heatmaps, stacked area distributions, dual-direction I/O vectors.
3. **Smart App Footprint**: Process grouping by application, container, or systemd unit with root-cause badges.
4. **Actionable Remediation**: Every insight contains evidence, confidence score, and a safe copyable command or confirmation key.

## 2. Color Palette & Typography
- **Background**: Deep Ink `#0d1117` / `#161b22`
- **Primary Hero / Accent**: Cyan Glow `#00e5ff` / Royal Blue `#3b82f6`
- **Health / Normal**: Emerald `#10b981`
- **Warning / Attention**: Amber `#f59e0b`
- **Danger / Critical**: Crimson Rose `#f43f5e`
- **Muted / Secondary**: Slate `#64748b`
- **Typography**: Clean UTF-8 box drawing (`┌ ─ ┐ │ └ ┘`), Unicode Block/Braille sparklines (` ▂▃▄▅▆▇█`), zero childish emojis.

## 3. Responsive Wireframe (Min 100x30)
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ SYSNARRATOR v0.2.0  [HEALTH SCORE: 88/100 EXCELLENT]  host: laptop  Linux 6.8 (x86_64)   │
│ CPU: 18% ↗  |  RAM: 42% →  |  DSK: 64% →  |  NET: 12KB/s ↗  |  TEMP: 48°C →  |  BAT: 85%│
├────────────────────────────────┬───────────────────────────────────────────────────────┤
│ LIVE NARRATIVE & INSIGHTS CARDS│ MULTI-CORE HEAT STRIP & RESOURCE VECTORS              │
│                                │ Core [ ▃█ ▂▅  ] avg 24% | Memory Stack: [Cached|Used] │
│ [CRITICAL] Root Disk (95%)     │ IO Vect: R: 0.1MB/s  W: 1.2MB/s [==>                ] │
│ Evidence: /var/log/journal     │                                                       │
│ Action: journalctl --vacuum    │ SMART APP FOOTPRINT (Grouped Context)                 │
│                                │ > Brave Browser   (18 procs | 3.4 GB | 14% CPU)       │
│ [INFO] D-State I/O Hold        │ > IDE / Editor    (12 procs | 2.1 GB |  8% CPU)       │
│ 1 process waiting on disk lock │ > MySQL Service   ( 1 proc  | 420 MB |  1% CPU)       │
├────────────────────────────────┴───────────────────────────────────────────────────────┤
│ [1] Story  [2] Processes Table  [3] Time Travel  [4] Systemd Units  [Ctrl+P] Actions   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Architecture Plan & Phasing
1. **Phase 1**: MetricStore (thread-safe ring buffers, 10 min historical snapshots at 1s intervals, trend slopes).
2. **Phase 2**: Original Textual TUI Application (`sysnarrator/tui/`) with responsive layout, real-time narration panel, heat strips, and action hooks.
3. **Phase 3**: Smart Process grouping (by application, tree, flat) with detail drawer.
4. **Phase 4**: Root-cause engine, forecasts (disk exhaustion ETA, memory leak slope), baseline anomaly detection.
5. **Phase 5**: Time travel scrub, systemd service diagnostics, export reports (`--export html/md/json`).
6. **Phase 6**: Verification, pytest coverage, user documentation, and PyPI readiness.
