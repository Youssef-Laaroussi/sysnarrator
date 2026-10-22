"""
Script to capture real SVG/PNG screenshots of the SysNarrator TUI tabs using Textual's Pilot.
Produces proof screenshots for: Overview, Processes, Insights, System, and Timeline tabs.
"""

import asyncio
from sysnarrator.tui import SysNarratorApp
from textual.widgets import TabbedContent

async def capture_all_tabs():
    app = SysNarratorApp(demo_mode=True)
    async with app.run_test(size=(120, 36)) as pilot:
        await pilot.pause(0.5)

        # 1. Overview Tab Screenshot
        app.save_screenshot("docs/screenshots/overview.svg")
        print("Captured overview.svg")

        # 2. Processes Tab Screenshot
        tabs = app.query_one(TabbedContent)
        tabs.active = "tab_processes"
        await pilot.pause(0.5)
        app.save_screenshot("docs/screenshots/processes.svg")
        print("Captured processes.svg")

        # 3. Insights Tab Screenshot
        tabs.active = "tab_insights"
        await pilot.pause(0.5)
        app.save_screenshot("docs/screenshots/insights.svg")
        print("Captured insights.svg")

        # 4. System Tab Screenshot
        tabs.active = "tab_system"
        await pilot.pause(0.5)
        app.save_screenshot("docs/screenshots/system.svg")
        print("Captured system.svg")

        # 5. Timeline Tab Screenshot
        tabs.active = "tab_timeline"
        await pilot.pause(0.5)
        app.save_screenshot("docs/screenshots/timeline.svg")
        print("Captured timeline.svg")

if __name__ == "__main__":
    asyncio.run(capture_all_tabs())
