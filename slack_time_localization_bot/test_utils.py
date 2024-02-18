import pytest

from slack_time_localization_bot.utils import sanitize_message_text

TEST_SANITIZE_MESSAGE_TEXT = [
    ("Let's meet a *12:30 UTC*.", "Let's meet a 12:30 UTC."),
    ("Let's meet a _12:30 UTC_.", "Let's meet a 12:30 UTC."),
]


@pytest.mark.parametrize("text,expected", TEST_SANITIZE_MESSAGE_TEXT)
def test_sanitize_message_text(text, expected):
    assert sanitize_message_text(text) == expected
