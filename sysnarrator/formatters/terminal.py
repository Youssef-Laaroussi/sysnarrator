"""Terminal Output Formatter with colors"""
import sys


class TerminalFormatter:
    """Formats output for terminal display with ANSI colors"""

    class Colors:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        DIM = "\033[2m"
        RED = "\033[91m"
        YELLOW = "\033[93m"
        GREEN = "\033[92m"
        CYAN = "\033[96m"
        MAGENTA = "\033[95m"
        WHITE = "\033[97m"

    LEVEL_COLORS = {
        'critical': Colors.RED,
        'warning': Colors.YELLOW,
        'ok': Colors.GREEN,
        'info': Colors.CYAN,
    }

    @classmethod
    def format_message(cls, message, level='info', no_color=False):
        """Format a single message with color if appropriate"""
        if no_color or not sys.stdout.isatty():
            return message
        color = cls.LEVEL_COLORS.get(level, cls.Colors.RESET)
        return f"{color}{message}{cls.Colors.RESET}"

    @classmethod
    def format_header(cls, text, no_color=False):
        """Format a section header"""
        if no_color:
            return f"  [{text.upper()}]"
        return f"  {cls.Colors.BOLD}{cls.Colors.WHITE}{text.upper()}{cls.Colors.RESET}"

    @classmethod
    def format_separator(cls):
        """Format a visual separator"""
        return f"{cls.Colors.CYAN}{'═'*60}{cls.Colors.RESET}"

    @classmethod
    def format_messages(cls, messages, no_color=False):
        """Format a list of messages, grouped by category"""
        output = []
        last_category = None

        for msg in messages:
            category = msg.get('category', '')
            text = msg['text']
            level = msg.get('level', 'info')

            if category and category != last_category:
                output.append(cls.format_header(category, no_color))
                last_category = category

            formatted = cls.format_message(text, level, no_color)
            output.append(f"  {formatted}")

        return "\n".join(output)
