import re


def sanitize_message_text(message: str) -> str:
    """Remove some mrkdwn text formatting character to facilitate temporal expression parsing."""
    return re.sub("[*_]", "", message)
