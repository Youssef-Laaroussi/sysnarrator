"""Plain Text Output Formatter"""


class PlainFormatter:
    """Formats output as plain text without colors or special formatting"""

    @staticmethod
    def format_message(message, level='info'):
        """Format a single message as plain text"""
        return message

    @staticmethod
    def format_header(text):
        """Format a section header as plain text"""
        return f"  [{text.upper()}]"

    @staticmethod
    def format_separator():
        """Format a visual separator"""
        return f"{'═'*60}"

    @staticmethod
    def format_messages(messages):
        """Format a list of messages as plain text"""
        output = []
        last_category = None

        for msg in messages:
            category = msg.get('category', '')
            text = msg['text']

            if category and category != last_category:
                output.append(PlainFormatter.format_header(category))
                last_category = category

            output.append(f"  {text}")

        return "\n".join(output)
