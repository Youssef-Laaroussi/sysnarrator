"""
Custom Braille and Sparkline chart widgets for Textual.
Zero-dependency, high-density terminal charting with area fill, auto-scaling,
threshold lines and gradient coloration.
"""

from typing import List, Optional, Tuple
from textual.widget import Widget
from textual.reactive import reactive
from rich.text import Text
from rich.style import Style


# Braille Unicode: 2 columns x 4 rows per character
# Dot weights:
# Col 0: row 0=0x1, row 1=0x2, row 2=0x4, row 3=0x40
# Col 1: row 0=0x8, row 1=0x10, row 2=0x20, row 3=0x80
BRAILLE_BASE = 0x2800
ROW_BITS_LEFT = [0x1, 0x2, 0x4, 0x40]
ROW_BITS_RIGHT = [0x8, 0x10, 0x20, 0x80]

SPARK_CHARS = " ▂▃▄▅▆▇█"


def sparkline_string(values: List[float], width: Optional[int] = None, min_val: float = 0.0, max_val: float = 100.0) -> str:
    """Generate a 1-line block sparkline."""
    if not values:
        return "N/A"
    vals = list(values)
    if width and len(vals) > width:
        vals = vals[-width:]
    elif width and len(vals) < width:
        vals = [vals[0]] * (width - len(vals)) + vals

    res = []
    diff = max_val - min_val if max_val != min_val else 1.0
    for v in vals:
        ratio = max(0.0, min(1.0, (v - min_val) / diff))
        idx = int(ratio * 7.99)
        res.append(SPARK_CHARS[idx])
    return "".join(res)


class BrailleAreaChart(Widget):
    """
    High-resolution 2D chart using Braille sub-pixel matrices.
    Renders area charts with threshold lines and gradient coloring.
    """

    data: reactive[List[float]] = reactive(list, always_update=True)
    threshold: reactive[Optional[float]] = reactive(None)
    min_val: reactive[float] = reactive(0.0)
    max_val: reactive[float] = reactive(100.0)
    title: reactive[str] = reactive("")

    def __init__(
        self,
        title: str = "",
        min_val: float = 0.0,
        max_val: float = 100.0,
        threshold: Optional[float] = None,
        color_scheme: str = "cyan",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.threshold = threshold
        self.color_scheme = color_scheme

    def render(self) -> Text:
        w = max(10, self.size.width - 2)
        h = max(3, self.size.height - 1)

        result = Text()
        if self.title:
            result.append(f"{self.title}\n", style="bold white")

        if not self.data:
            result.append(" [Waiting for metric data...]\n", style="dim italic")
            return result

        # Each char is 2 data points horizontally and 4 pixels vertically
        points_needed = w * 2
        raw_points = list(self.data)[-points_needed:]
        if len(raw_points) < points_needed:
            pad = [raw_points[0] if raw_points else 0.0] * (points_needed - len(raw_points))
            raw_points = pad + raw_points

        # Grid of braille cells (h rows, w cols)
        grid = [[0 for _ in range(w)] for _ in range(h)]
        total_pixel_height = h * 4

        # Plot area
        diff = self.max_val - self.min_val if self.max_val != self.min_val else 1.0
        for x_idx, val in enumerate(raw_points):
            char_x = x_idx // 2
            col_in_char = x_idx % 2

            ratio = max(0.0, min(1.0, (val - self.min_val) / diff))
            fill_pixels = int(ratio * total_pixel_height)

            for p in range(fill_pixels):
                py = total_pixel_height - 1 - p
                char_y = py // 4
                sub_y = py % 4
                if 0 <= char_y < h and 0 <= char_x < w:
                    bit = ROW_BITS_LEFT[sub_y] if col_in_char == 0 else ROW_BITS_RIGHT[sub_y]
                    grid[char_y][char_x] |= bit

        # Render rows with gradient
        for y in range(h):
            row_ratio = (h - y) / h
            # Color based on vertical height/severity
            if self.color_scheme == "thermal":
                if row_ratio > 0.8:
                    style_str = "bold red"
                elif row_ratio > 0.6:
                    style_str = "yellow"
                else:
                    style_str = "green"
            elif self.color_scheme == "magenta":
                style_str = "magenta"
            elif self.color_scheme == "blue":
                style_str = "cyan" if row_ratio > 0.5 else "blue"
            else:
                style_str = "bold cyan" if row_ratio > 0.7 else "cyan"

            line_chars = []
            for x in range(w):
                cell_bits = grid[y][x]
                if cell_bits == 0:
                    line_chars.append(" ")
                else:
                    line_chars.append(chr(BRAILLE_BASE + cell_bits))

            row_str = "".join(line_chars)
            # Add threshold indicator if applicable
            result.append(row_str, style=style_str)
            result.append("\n")

        return result
