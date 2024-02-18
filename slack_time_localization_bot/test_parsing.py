import datetime
from datetime import time
from zoneinfo import ZoneInfo

import pytest

from slack_time_localization_bot.parsing import (
    detect_language,
    text_to_temporal_expressions,
    detect_timezone,
)

TEST_DETECT = [
    ("Let us meet at 11 am or 1 pm.", "EN"),
    ("Lass uns um 11 oder 13 Uhr treffen.", "DE"),
]


@pytest.mark.parametrize("test_input,expected", TEST_DETECT)
def test_detect_language(test_input, expected):
    assert detect_language(test_input) == expected


TEST_DETECT_TZ = [
    ("Let us meet at 11 am.", None),
    ("Let us meet at 11 UTC.", ZoneInfo("UTC")),
]


@pytest.mark.parametrize("test_input,expected", TEST_DETECT_TZ)
def test_detect_timezone(test_input, expected):
    assert detect_timezone(test_input) == expected


REFERENCE_TZ = ZoneInfo("CET")
REFERENCE_DATETIME = datetime.datetime(2023, 2, 17, 18, 17, tzinfo=REFERENCE_TZ)


def today(hour: int = 0, minute: int = 0, tzinfo=REFERENCE_TZ) -> datetime.datetime:
    return datetime.datetime.combine(
        REFERENCE_DATETIME, time(hour, minute), tzinfo=tzinfo
    )


def tomorrow(hour: int = 0, minute: int = 0, tzinfo=REFERENCE_TZ) -> datetime.datetime:
    tomorrow_datetime = REFERENCE_DATETIME + datetime.timedelta(days=1)
    return datetime.datetime.combine(
        tomorrow_datetime, time(hour, minute), tzinfo=tzinfo
    ).astimezone(REFERENCE_TZ)


TEST_TEXT_TO_TIMES = [
    ("12:00 UTC", [tomorrow(12, tzinfo=ZoneInfo("UTC"))]),
    ("Lets meet at 12:00", [tomorrow(12)]),
    ("Let us meet at 11 am or 1 pm.", [tomorrow(11), tomorrow(13)]),
    ("Let us meet today at 8 o'clock pm.", [today(20)]),
    (
        "Let us meet today at 8 o'clock pm UTC.",
        [today(20, tzinfo=ZoneInfo("UTC"))],
    ),
    (
        "Let us meet today at 20:53 UTC.",
        [today(20, 53, tzinfo=ZoneInfo("UTC"))],
    ),
    ("Lass uns morgen um 11 oder 13 Uhr treffen.", [tomorrow(11), tomorrow(13)]),
    ("Lasst uns heute um 11 treffen.", [today(11)]),
    ("Lasst uns morgen um 11:00 EST treffen.", [tomorrow(11, tzinfo=ZoneInfo("EST"))]),
]


@pytest.mark.parametrize("test_input,expected", TEST_TEXT_TO_TIMES)
def test_text_to_times(test_input, expected):
    results = text_to_temporal_expressions(test_input, REFERENCE_DATETIME)
    all_datetimes = [result.datetime for result in results]
    assert all_datetimes == expected
