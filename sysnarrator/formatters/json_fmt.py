"""JSON Output Formatter"""
import json
from datetime import datetime
import os


class JSONFormatter:
    """Formats output as JSON for programmatic consumption"""

    @staticmethod
    def format_messages(messages):
        """Convert messages to JSON-friendly structure"""
        return messages

    @staticmethod
    def format_report(messages, metadata=None):
        """Format a complete report as JSON"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'hostname': os.uname().nodename,
            'messages': messages,
        }

        if metadata:
            report.update(metadata)

        return report

    @staticmethod
    def to_json_string(data, indent=2, ensure_ascii=False):
        """Convert data to JSON string"""
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

    @staticmethod
    def to_json_compact(data, ensure_ascii=False):
        """Convert data to compact JSON string"""
        return json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii)
