"""Professional Color Formatter - Ubuntu System Analysis"""
import sys


class ProfessionalFormatter:
    """
    Professional system analysis formatter with modern color scheme.
    Colors: Orange (#FF9500), Blue (#0A84FF), Gray (#5E5CE6), Green (#34C759)
    """

    class Colors:
        # Professional ANSI colors
        RESET = "\033[0m"
        BOLD = "\033[1m"
        DIM = "\033[2m"
        
        # Primary colors - Professional palette
        ORANGE = "\033[38;5;208m"      # Orange (#FF9500)
        BLUE = "\033[38;5;33m"         # Blue (#0A84FF)
        GRAY = "\033[38;5;240m"        # Gray
        GREEN = "\033[38;5;76m"        # Green
        RED = "\033[38;5;196m"         # Red
        YELLOW = "\033[38;5;226m"      # Yellow
        
        # Background colors
        BG_ORANGE = "\033[48;5;208m"
        BG_BLUE = "\033[48;5;33m"
        BG_DARK = "\033[48;5;235m"

    LEVEL_COLORS = {
        'critical': Colors.RED,
        'warning': Colors.YELLOW,
        'ok': Colors.GREEN,
        'info': Colors.BLUE,
        'expert': Colors.ORANGE,
    }

    CATEGORY_COLORS = {
        'CPU': Colors.ORANGE,
        'RAM': Colors.BLUE,
        'Disk': Colors.GRAY,
        'Réseau': Colors.BLUE,
        'Network': Colors.BLUE,
        'Température': Colors.RED,
        'Temperature': Colors.RED,
        'Système': Colors.GRAY,
        'System': Colors.GRAY,
        'Processus': Colors.ORANGE,
        'Processes': Colors.ORANGE,
        'Recommandations': Colors.ORANGE,
        'Recommendations': Colors.ORANGE,
        'Analyse': Colors.BLUE,
        'Analysis': Colors.BLUE,
    }

    @classmethod
    def format_title(cls, text, no_color=False):
        """Format main title with professional styling"""
        if no_color:
            return f"\n{'═'*70}\n  {text.upper()}\n{'═'*70}"
        return f"\n{cls.Colors.ORANGE}{cls.Colors.BOLD}{'═'*70}{cls.Colors.RESET}\n  {cls.Colors.BOLD}{cls.Colors.ORANGE}{text.upper()}{cls.Colors.RESET}\n{cls.Colors.ORANGE}{'═'*70}{cls.Colors.RESET}"

    @classmethod
    def format_header(cls, text, no_color=False):
        """Format section header with category color"""
        color = cls.CATEGORY_COLORS.get(text, cls.Colors.BLUE)
        if no_color:
            return f"\n  ► {text.upper()}"
        return f"\n  {color}{cls.Colors.BOLD}► {text.upper()}{cls.Colors.RESET}"

    @classmethod
    def format_message(cls, message, level='info', no_color=False):
        """Format individual message with appropriate color"""
        if no_color:
            return message
        color = cls.LEVEL_COLORS.get(level, cls.Colors.BLUE)
        return f"{color}{message}{cls.Colors.RESET}"

    @classmethod
    def format_expert_tip(cls, title, content, no_color=False):
        """Format expert tip/recommendation"""
        if no_color:
            return f"\n  💡 {title}:\n     {content}"
        return f"\n  {cls.Colors.ORANGE}{cls.Colors.BOLD}💡 {title}:{cls.Colors.RESET}\n     {cls.Colors.ORANGE}{content}{cls.Colors.RESET}"

    @classmethod
    def format_metric(cls, label, value, unit="", level="info", no_color=False):
        """Format a metric with label and value"""
        color = cls.LEVEL_COLORS.get(level, cls.Colors.BLUE)
        if no_color:
            return f"  {label}: {value} {unit}"
        return f"  {cls.Colors.BOLD}{label}:{cls.Colors.RESET} {color}{value}{cls.Colors.RESET} {unit}"

    @classmethod
    def format_health_bar(cls, percent, width=30, no_color=False):
        """Format a health bar visualization"""
        filled = int(percent / 100 * width)
        empty = width - filled
        
        if percent >= 90:
            bar_color = cls.Colors.RED
            health = "CRITICAL"
        elif percent >= 70:
            bar_color = cls.Colors.YELLOW
            health = "WARNING"
        elif percent >= 50:
            bar_color = cls.Colors.ORANGE
            health = "MODERATE"
        else:
            bar_color = cls.Colors.GREEN
            health = "HEALTHY"

        if no_color:
            bar = "█" * filled + "░" * empty
            return f"  {bar} {percent:.0f}% - {health}"
        
        bar = f"{bar_color}{'█' * filled}{cls.Colors.RESET}{'░' * empty}"
        return f"  {bar} {bar_color}{percent:.0f}%{cls.Colors.RESET} - {bar_color}{health}{cls.Colors.RESET}"

    @classmethod
    def format_system_score(cls, score, no_color=False):
        """Format overall system health score"""
        if score >= 90:
            status = "EXCELLENT"
            color = cls.Colors.GREEN
        elif score >= 75:
            status = "GOOD"
            color = cls.Colors.GREEN
        elif score >= 60:
            status = "FAIR"
            color = cls.Colors.ORANGE
        elif score >= 40:
            status = "POOR"
            color = cls.Colors.YELLOW
        else:
            status = "CRITICAL"
            color = cls.Colors.RED

        if no_color:
            return f"\n  SYSTEM HEALTH SCORE: {score:.0f}/100 - {status}"
        
        return f"\n  {color}{cls.Colors.BOLD}SYSTEM HEALTH SCORE: {score:.0f}/100 - {status}{cls.Colors.RESET}"

    @classmethod
    def format_messages(cls, messages, no_color=False):
        """Format a complete message list"""
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

    @classmethod
    def format_divider(cls, char="─", no_color=False):
        """Format a visual divider"""
        if no_color:
            return f"  {char * 64}"
        return f"  {cls.Colors.GRAY}{char * 64}{cls.Colors.RESET}"
