import datetime
from datetime import time
from zoneinfo import ZoneInfo

import pytest

from slack_time_localization_bot.parsing import (
    detect_language,
    text_to_temporal_expressions,
    detect_single_timezone,
    TemporalIntervalExpression,
)

TEST_DETECT = [
    ("Let us meet at 11 am or 1 pm.", "EN"),
    ("Lass uns um 11 oder 13 Uhr treffen.", "DE"),
    ("F", "EN"),
    ("10:00 GMT", "EN"),
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
    assert detect_single_timezone(test_input) == expected


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
    ("12:00 UTC", [tomorrow(12, tzinfo=ZoneInfo("UTC"))], True),
    ("10:00 GMT", [tomorrow(10, tzinfo=ZoneInfo("GMT"))], True),
    ("Lets meet at 12:00", [tomorrow(12)], True),
    ("Let us meet at 11 am or 1 pm.", [tomorrow(11), tomorrow(13)], True),
    ("Let us meet today at 8 o'clock pm.", [today(20)], True),
    (
        "Let us meet today at 8 o'clock pm UTC.",
        [today(20, tzinfo=ZoneInfo("UTC"))],
        True,
    ),
    (
        "Let us meet today at 20:53 UTC.",
        [today(20, 53, tzinfo=ZoneInfo("UTC"))],
        True,
    ),
    (
        "15:00 (UTC) / 16:00 (CET)",
        [
            tomorrow(15, 00, tzinfo=ZoneInfo("UTC")),
            tomorrow(16, 00, tzinfo=ZoneInfo("CET")),
        ],
        True,
    ),
    ("Lass uns morgen um 11 oder 13 Uhr treffen.", [tomorrow(11), tomorrow(13)], True),
    ("Lasst uns heute um 11 treffen.", [today(11)], True),
    (
        "Lasst uns morgen um 11:00 EST treffen.",
        [tomorrow(11, tzinfo=ZoneInfo("EST"))],
        True,
    ),
    ("at 11:15 UTC / 12:15 CET", [
        tomorrow(11, 15, tzinfo=ZoneInfo("UTC")),
        tomorrow(12, 15, tzinfo=ZoneInfo("CET")),
    ], True),
    # invalid times
    ("let's upgrade from Ubuntu 16.04", [], True),
    # intervals
    ("from the one", [], True),
    (
        "starting between at 05:00 and 07:12 UTC",
        [
            tomorrow(5, 00, tzinfo=ZoneInfo("UTC")),
            tomorrow(7, 12, tzinfo=ZoneInfo("UTC")),
        ],
        True,
    ),
    (
        "starting between at 05:00 and 07:12 UTC",
        [
            today(17, 00, tzinfo=ZoneInfo("UTC")),
            today(19, 12, tzinfo=ZoneInfo("UTC")),
        ],
        False,
    ),
    (
        "starting between at 5 and 7",
        [
            tomorrow(5, 00),
            tomorrow(7, 00),
        ],
        True,
    ),
    (
        "for a few minutes starting at 12:15 CET",
        [
            tomorrow(12, 15, tzinfo=ZoneInfo("CET")),
            tomorrow(12, 18, tzinfo=ZoneInfo("CET")),
        ],
        True,
    ),
    # half intervals
    (
        "since around 9:40 UTC",
        [
            tomorrow(9, 40, tzinfo=ZoneInfo("UTC")),
        ],
        True,
    ),
    (
        "until around 9:40 UTC",
        [
            tomorrow(9, 40, tzinfo=ZoneInfo("UTC")),
        ],
        True,
    ),
]


@pytest.mark.parametrize(
    "test_input,expected,prefer_24h_interpretation", TEST_TEXT_TO_TIMES
)
def test_text_to_times(test_input, expected, prefer_24h_interpretation):
    results = text_to_temporal_expressions(
        test_input, REFERENCE_DATETIME, prefer_24h_interpretation
    )
    all_datetimes = [result.datetime for result in results]
    all_datetimes += [
        result.end_datetime
        for result in results
        if isinstance(result, TemporalIntervalExpression)
    ]
    assert all_datetimes == expected


TEST_TEXT_TO_TIMES_TIMEZONES = [
    (
        "15:00 (UTC) / 16:00 (CET)",
        [ZoneInfo("UTC"), ZoneInfo("CET")],
        True,
    ),
    (
        "15:00 (utc) / 16:00 (cet)",
        [ZoneInfo("UTC"), ZoneInfo("CET")],
        True,
    ),
]


@pytest.mark.parametrize(
    "test_input,expected,prefer_24h_interpretation", TEST_TEXT_TO_TIMES_TIMEZONES
)
def test_text_to_times_timezones(test_input, expected, prefer_24h_interpretation):
    results = text_to_temporal_expressions(
        test_input, REFERENCE_DATETIME, prefer_24h_interpretation
    )
    all_timezones = [result.timezone for result in results]
    assert all_timezones == expected
